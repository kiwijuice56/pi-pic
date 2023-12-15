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
will_autostart = False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    if "update" in message.content or "Update" in message.content:
        pass
    elif "clear" in message.content or "Clear" in message.content:
        delete_images()
    else:
        for attachment in message.attachments:
            print("Image downloading...")
            await attachment.save(os.path.join(DIR, "img", attachment.filename))
            print("Image downloaded!")
    load_images()
    await bot.change_presence(activity=discord.Game(name=get_status()))


def delete_images():
    for file in os.listdir(os.path.join(program_dir, "img")):
        os.remove(os.path.join(program_dir, "img", file))
    load_images()
    print("All images deleted.")


def load_images():
    images.clear()
    for file in os.listdir(os.path.join(program_dir, "img")):
        image = Image.open(os.path.join(program_dir, "img", file))
        images.append(ImageOps.fit(image, inky.resolution))


def update_screen(): 
    load_images()
    print("Refreshing screen...")
    if len(images) == 0:
        print("No images to show.")
        return    
    inky.set_image(random.choice(images), saturation=picture_saturation)
    inky.show()
    

def update_loop(seconds):
    while True:
        update_screen()
        sleep(seconds)


def get_status():
    return str(len(images)) + " images")

# Initialize directory
program_dir = os.path.dirname(__file__)

# Initialize Inky program
images = []
load_images()
inky = Inky(resolution=inky_resolution)

# Initialize Discord bot
bot = commands.Bot(command_prefix="%", intents=discord.Intents().all(), activity=discord.Game(name=get_status()))
channel = bot.get_channel(int(open(os.path.join(program_dir, "CHANNEL.txt"), "r").readline()))

# To allow the Pi to connect to the wifi before the Discord bot logs in
if will_autostart:
    sleep(8)

update_thread = Thread(target=update_loop, args=(delay_seconds,))
update_thread.start()
bot.run(open(os.path.join(program_dir, "TOKEN.txt"), "r").readline())
