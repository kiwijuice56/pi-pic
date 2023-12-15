import discord
from discord.ext import commands
import aiohttp, os
from inky.inky_uc8159 import Inky
from PIL import Image, ImageOps
from threading import Thread
from time import sleep
import random


# Program parameters... change these to fit your usage
delay_seconds = 60 * 25
picture_saturation = 0.55
inky_resolution=(640,400) # Check your device specifications
login_delay = False # Set to True if allowing the program to run at boot

# Initialize objects
program_dir = os.path.dirname(__file__)
inky = Inky(resolution=inky_resolution)
bot = commands.Bot(command_prefix="%", intents=discord.Intents().all(), activity=discord.Game(name="hello world!"))


@bot.event
async def on_message(message):
    if "clear" in message.content.lower():
        for file in os.listdir(os.path.join(program_dir, "img")):
            os.remove(os.path.join(program_dir, "img", file))
        await bot.change_presence(activity=discord.Game(name="image(s) deleted :("))
    else:
        for attachment in message.attachments:
            await attachment.save(os.path.join(program_dir, "img", attachment.filename))
        await bot.change_presence(activity=discord.Game(name="image(s) uploaded :)"))
    

def update_loop(seconds):
    while True:
        images = []
        for file in os.listdir(os.path.join(program_dir, "img")):
            image = Image.open(os.path.join(program_dir, "img", file))
            images.append(ImageOps.fit(image, inky.resolution))
        if len(images) == 0:
            return    
        inky.set_image(random.choice(images), saturation=picture_saturation)
        inky.show()
        sleep(seconds)


if login_delay:
    sleep(8)

update_thread = Thread(target=update_loop, args=(delay_seconds,))
update_thread.start()
bot.run(open(os.path.join(program_dir, "TOKEN.txt"), "r").readline())
