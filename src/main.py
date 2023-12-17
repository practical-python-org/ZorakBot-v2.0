import os
import sys
import discord
from discord.ext import commands

from logger import *


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=intents)


async def load_cogs(robot: commands.Bot) -> None:
    """
    Loads the directories under the /cogs/ folder,
    then digs through those directories and loads the cogs.

    We do not load files starting with _ and the templates folder.
    """
    log_info("Loading Cogs...")
    for directory in os.listdir("./cogs"):
        if not directory.startswith("_") and directory != "templates":
            for file in os.listdir(f"./cogs/{directory}"):
                if file.endswith('.py') and not file.startswith("_"):
                    log_debug(f"Loading Cog: \\{directory}\\{file}")
                    await robot.load_extension(f"cogs.{directory}.{file[:-3]}")
    log_info(" - Success.")


def load_key_and_run():
    """
    Loads the bot key as the first arg when running the bot OR from an env variable.
    For example:
        "python __main__.py BOT_TOKEN_HERE"
    """
    if len(sys.argv) > 1:  # Check args for the token first
        token = sys.argv[1].replace('TOKEN=','')
        log_debug('Loading Token from arg.')
        bot.run(token)

    elif os.environ['TOKEN'] is not None:  # if not in args, check the env vars
        log_debug('Loading Token from environment variable.')
        bot.run(os.environ['TOKEN'])

    else:
        log_critical('You must include a bot token...')
        log_critical("TOKEN must be in the .env file")
        log_critical('OR you must run the bot using: "python __main__.py TOKEN=YOUR_DISCORD_TOKEN"')


@bot.event
async def setup_hook() -> None:
    """
    The setup_hook executes before the bot logs in.
    """
    log_debug("Executing set up hook...")
    await load_cogs(bot)


@bot.event
async def on_ready() -> None:
    """
    The on_ready is executed AFTER the bot logs in.
    """
    log_debug("Executing on_ready event.")
    log_info(f'Logged in as {bot.user.name} - ({bot.user.id})')


load_key_and_run()
