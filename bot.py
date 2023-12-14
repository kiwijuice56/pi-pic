import discord
from discord.ext import commands

# Required to download images and handle file system
import aiohttp, os

# Required for electronic ink display
from inky.inky_uc8159 import Inky
from PIL import Image, ImageOps

# Required for refreshing screen
from threading import Thread
from time import sleep
import random

# Discord bot parameters
DIR = os.path.dirname(__file__)
CHANNEL_ID = int(open(os.path.join(DIR, "CHANNEL.txt"), "r").readline())
TOKEN = open(os.path.join(DIR, "TOKEN.txt"), "r").readline()

# Discord bot initialization
channel = None
bot = commands.Bot(command_prefix="%", intents=discord.Intents().all())

# Image initialization
images = []
inky = Inky(resolution=(640,400))


@bot.event
async def on_ready():
    global channel
    channel = bot.get_channel(CHANNEL_ID)
    print(f"Logged in as {bot.user}")
    load_images()


@bot.event
async def on_message(message):
    for attachment in message.attachments:
        print("Image downloading...")
        await attachment.save(os.path.join(DIR, "img", attachment.filename))
        print("Image downloaded!")
    load_images()


def load_images():
    images.clear()
    for file in os.listdir(os.path.join(DIR, "img")):
        image = Image.open(os.path.join(DIR, "img", file))
        ImageOps.fit(image, inky.resolution)
        images.append(image)


def update_screen(): 
    load_images()
    print("Refreshing screen...")
    if len(images) == 0:
        print("No images to show")
        return    
    inky.set_image(random.choice(images), saturation=0.5)
    inky.show()
    

def update_loop(seconds):
    update_screen()
    sleep(seconds)


update_thread = Thread(target=update_loop, args=(60,))
update_thread.start()
bot.run(TOKEN)
