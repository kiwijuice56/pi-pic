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

# Image initialization
images = []
load_images()
inky = Inky(resolution=(640,400))


# Discord bot initialization
channel = None
bot = commands.Bot(command_prefix="%", intents=discord.Intents().all(), activity=discord.Streaming(name=(str(len(images)) + " images")))


@bot.event
async def on_ready():
    global channel
    channel = bot.get_channel(CHANNEL_ID)
    print(f"Logged in as {bot.user}")
    load_images()


@bot.event
async def on_message(message):
    if "clear" in message.content or "Clear" in message.content:
        delete_images()
        return
    for attachment in message.attachments:
        print("Image downloading...")
        await attachment.save(os.path.join(DIR, "img", attachment.filename))
        print("Image downloaded!")
    load_images()
    await bot.change_presence(activity=discord.Streaming(name=(str(len(images)) + " images")))


def delete_images():
    for file in os.listdir(os.path.join(DIR, "img")):
        os.remove(os.path.join(DIR, "img", file))
    load_images()
    print("All images deleted.")


def load_images():
    images.clear()
    for file in os.listdir(os.path.join(DIR, "img")):
        image = Image.open(os.path.join(DIR, "img", file))
        images.append(ImageOps.fit(image, inky.resolution))


def update_screen(): 
    load_images()
    print("Refreshing screen...")
    if len(images) == 0:
        print("No images to show.")
        return    
    inky.set_image(random.choice(images), saturation=0.5)
    inky.show()
    

def update_loop(seconds):
    while True:
        update_screen()
        sleep(seconds)

# Uncomment for autostart
# sleep(10)

update_thread = Thread(target=update_loop, args=(900,))
update_thread.start()
bot.run(TOKEN)
