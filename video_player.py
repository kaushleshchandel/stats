import shlex
import time
import subprocess
import digitalio
import board
import time
import RPi.GPIO as GPIO #Python Package Reference: https://pypi.org/project/RPi.GPIO/

# Pin definition
b1_pin = 24
b2_pin = 25
b3_pin = 26
b4_pin = 27
b5_pin = 28

# Suppress warnings
GPIO.setwarnings(False)
# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)
# Use pullup resistor so that the pin is not floating
GPIO.setup(shutdown_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(reboot_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# function to shutdown Pi
def shut_down():
    print("shutting down")
    command = "/usr/bin/sudo /sbin/shutdown -h now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


while True:

    # Check the buttons value if LOW or HIGH
    b1 = GPIO.input(b1_pin)
    b2 = GPIO.input(b2_pin)
    b3 = GPIO.input(b3_pin)
    b4 = GPIO.input(b4_pin)
    b5 = GPIO.input(b5_pin)

    # If Shutdown button is pressed
    if b1 == GPIO.LOW:
        # Keep checking for 5 seconds
        while GPIO.input(shutdown_pin) == GPIO.LOW:
            counter += 1
            time.sleep(0.01)
            msg = "Shutdown ? " + str(counter)
            print_shutdown_reboot(msg)
            if counter > 5:
                print_shutdown_reboot("Shutdown now...")
                shut_down()
    time.sleep(0.1)
