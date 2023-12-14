# pi-pic
Small script to configure my Rasberry Pi 4 Model B with the [Inky Impression 4" (7 colour ePaper/eInk HAT).](https://shop.pimoroni.com/products/inky-impression-4?variant=39599238807635) Utilizes a private Discord server and bot to receive images and cycle through them randomly.

![Example image](example.jpeg "Example")

## Set Up 
1) After connecting the Pi and Inky, install the following dependencies
```
sudo pip3 install inky
sudo pip3 install discord.py
sudo pip3 install pillow
```

2) Clone the repository 
```
sudo git clone https://github.com/kiwijuice56/pi-pic
```

3) Create a Discord bot and server. In the server, create a single channel where you will interface with the bot. Create two files in the pi-pic directory: `CHANNEL.txt` and `TOKEN.txt` and copy the Discord channel's ID and the bot's token into each file respectively.

4) Run the script
```
sudo python3 pi-pic/bot.py
```

5) (Optional) Create a service to start the script whenever the pi is rebooted:
```
sudo nano /lib/systemd/system/pipic.service
```
Insert the following text, replacing the username if necessary:
```
[Unit]
Description=Start Pi Picture Slideshow
After=network-online.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /home/pi/pi-pic/bot.py
Restart=always
User=pi

[Install]
WantedBy=network-online.target
```

Finally, enable the service using the following:
```
sudo systemctl enable pipic.service
```

## Usage
Send pictures in the selected channel to add them to the slideshow or send the text `clear` to remove all of the pictures. The slideshow will stop if there are no pictures.