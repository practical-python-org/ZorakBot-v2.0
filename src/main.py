import os
import discord
from discord.ext import commands

from logger import *


ZorakV2 = os.getenv("TOKEN")
prefix = os.getenv("PREFIX")

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


async def load_cogs(robot):
    """
    Loads the directories under the /cogs/ folder,
    then digs through those directories and loads the cogs.
    """
    log_info("Loading Cogs...")
    for directory in os.listdir("./cogs"):
        if not directory.startswith("_"):  # Makes sure __innit.py__ doesnt get called
            for file in os.listdir(f"./cogs/{directory}"):
                if file.endswith('.py') and not file.startswith("_"):
                    log_info(f"Loading Cog: \\{directory}\\{file}")
                    await robot.load_extension(f"cogs.{directory}.{file[:-3]}")
    log_info(" - Success.")


@bot.event
async def setup_hook() -> None:
    """
    The setup_hook executes before the bot logs in.
    """
    log_info("Executing set up hook...")
    await load_cogs(bot)


@bot.event
async def on_ready() -> None:
    """
    The on_ready is executed AFTER the bot logs in.
    """
    log_info("Executing on_ready event.")
    log_info(f'Logged in as {bot.user.name} - ({bot.user.id})')


bot.run(ZorakV2)
