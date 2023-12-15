# pi-pic
A script to configure my Rasberry Pi 4 Model B with the [Inky Impression 4" (7 colour ePaper/eInk HAT).](https://shop.pimoroni.com/products/inky-impression-4?variant=39599238807635) Utilizes a private Discord server and bot to receive images and cycle through them randomly.

![Example image](example.jpeg "Example")

## Set Up 
1) After connecting the Pi and Inky, install the following dependencies
```
sudo pip3 install inky[rpi,example-depends]
sudo pip3 install discord.py
sudo pip3 install pillow
```

2) Clone this repository 
```
sudo git clone https://github.com/kiwijuice56/pi-pic
```

3) Create a Discord bot and server. Create the file `TOKEN.txt` in the pi-pic directory and copy the Discord bot's token into it. 

4) Run the script
```
sudo python3 pi-pic/bot.py
```

5) (Optional) To allow the script to start up at boot, edit the file:
```
sudo nano /etc/rc.local
```
And add the following line of code right before the exit line:
```
python3 /home/pi/pi-pic/bot.py &
```
Finally, edit the parameters at the start of `bot.py` to fit your usage
```python
delay_seconds = 60 * 25
picture_saturation = 0.55
inky_resolution=(640,400) # Check your device specifications
login_delay = False # Set to True if allowing the program to run at boot
```

## Usage
Send pictures in any channel of the server to add them to the slideshow or send the text `clear` to remove all of the pictures. The slideshow will stop if there are no pictures. 