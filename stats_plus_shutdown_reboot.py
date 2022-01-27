# -*- coding: utf-8 -*-
# GPIO 23,24
#  ______________
# |           ---|
# | Reboot    |24|
# | Shutdown  |23|
# |           ---|
# |______________|
# Two buttons connected to the GPIO 24 & 23. 
# Screen displayes the stats
# When Reboot button is pressed for more than 5 seconds, system reboots
# When Reset button is pressed for more than 5 seconds, system Shuts down

import shlex
import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import time
import RPi.GPIO as GPIO #Python Package Reference: https://pypi.org/project/RPi.GPIO/

# Pin definition
shutdown_pin = 24
reboot_pin = 23

# Suppress warnings
GPIO.setwarnings(False)
# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)
# Use pullup resistor so that the pin is not floating
GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reboot_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000
# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 270

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font0 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Function restarts teh Raspberr PI
def restart():
    print("restarting Pi")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

# function to shutdown Pi
def shut_down():
    print("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

# Print the Stats or any other info
def print_info():
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # Shell scripts for system monitoring from here:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text.
    y = top
    draw.text((x, y), "** DEVICE NAME ***", font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1] + 10
    draw.text((x, y), IP, font=font, fill="#FFFFFF")
    y += font.getsize(IP)[1] + 4
    draw.text((x, y), CPU, font=font, fill="#FFFF00")
    y += font.getsize(CPU)[1] + 4
    draw.text((x, y), MemUsage, font=font0, fill="#00FF00")
    y += font.getsize(MemUsage)[1] + 4
    draw.text((x, y), Disk, font=font0, fill="#0000FF")
    y += font.getsize(Disk)[1] + 4
    draw.text((x, y), Temp, font=font0, fill="#FF00FF")

    cmd = "uptime -p"
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    uptime = "Uptime: " + str(p.communicate())[5:15]

    y += font.getsize(Temp)[1] + 4
    draw.text((x, y), uptime, font=font0, fill="#FF00FF")

    # Display image.
    disp.image(image, rotation)

def print_shutdown_reboot(caption):
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    y = 100
    draw.text((x, y), caption, font=font1, fill="#FF00FF")
    # Display image.
    disp.image(image, rotation)


while True:
    
    # Check the buttons value if LOW or HIGH
    bs = GPIO.input(shutdown_pin)
    br = GPIO.input(reboot_pin)
#    print(bs,br)
    
    # If Shutdown button is pressed
    if bs == GPIO.LOW:
        counter = 0
        # Keep checking for 5 seconds
        while GPIO.input(shutdown_pin) == GPIO.LOW:
            counter += 1
            time.sleep(0.5)
            msg = "Shutdown ? " + str(counter)
            print_shutdown_reboot(msg)
            if counter > 5:
                print_shutdown_reboot("Shutdown now...")
                shut_down()

    # shut_down()
    if br == GPIO.LOW:
        counter = 0
        # Keep checking for 5 seconds
        while GPIO.input(reboot_pin) == GPIO.LOW:
            counter += 1
            time.sleep(0.5)
            msg = "Reboot ? " + str(counter)
            print_shutdown_reboot(msg)
            if counter > 5:
                print_shutdown_reboot("Rebooting now...")
                restart()

    # If none of the buttons are pressed then display the stats
    if bs == GPIO.HIGH:
        if br == GPIO.HIGH:
            print_info()
    time.sleep(0.1)
