# stats
Instructions for LCD
https://github.com/IOT-MCU/Mini-PiTFT-for-Raspberry-Pi/wiki/Usage

```sudo pip3 install adafruit-circuitpython-rgb-display```
```sudo pip3 install --upgrade --force-reinstall spidev```


```sudo apt-get install python3-pip```

DejaVu TTF Font
Raspberry Pi usually comes with the DejaVu font already installed, but in case it didn't, you can run the following to install it:

```sudo apt-get install ttf-dejavu```

Pillow Library
We also need PIL, the Python Imaging Library, to allow graphics and using text with custom fonts. There are several system libraries that PIL relies on, so installing via a package manager is the easiest way to bring in everything:

```sudo apt-get install python3-pil```

NumPy Library
A recent improvement of the RGB_Display library makes use of NumPy for some additional speed. This can be installed with the following command:

```sudo apt-get install python3-numpy```

Setup startup 

create a file named app.sh

```sudo nano app.sh```


cd /
cd home/pi
sudo python app.py
cd /


```sudo chmod 755 app.sh```

Log direectory

```
mkdir logs
sudo crontab -e
```

Add to the end of file

@reboot sh /home/pi/app.sh >/home/pi/logs/cronlog 2>&1
