import os
import sys
import logging
import discord
from discord.ext import commands

from __logger__ import setup_logger
from db.database import init_db


logger = logging.getLogger(__name__)
setup_logger(level=int(os.getenv("LOG_LEVEL")), stream_logs=bool(os.getenv("STREAM_LOGS")))

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=os.getenv("PREFIX"), intents=intents)


async def load_cogs(robot: commands.Bot) -> None:
    """
    Loads the directories under the /cogs/ folder,
    then digs through those directories and loads the cogs.

    We do not load files starting with _ and the templates folder.
    """
    logger.info("Loading Cogs...")
    for directory in os.listdir("./src/cogs"):
        if not directory.startswith("_") and directory != "templates":
            for file in os.listdir(f"./src/cogs/{directory}"):
                if file.endswith('.py') and not file.startswith("_"):
                    logger.debug(f"Loading Cog: \\{directory}\\{file}")
                    try:
                        await robot.load_extension(f"cogs.{directory}.{file[:-3]}")
                    except Exception as e:
                        logger.warning("- - - Cog failed to load!!")
                        logger.warning(f"- - - {e}")
    logger.info("... Success.")


def connect_to_db(flag_db):
    healthy = False
    for attempt in range(5):
        if flag_db and not healthy:
            init_db(bot)
            logger.info(f"Healthchecking database...")
            if bot.db.healthcheck():
                return


@bot.event
async def setup_hook() -> None:
    """
    The setup_hook executes before the bot logs in.
    """
    logger.debug("Executing set up hook...")


@bot.event
async def on_ready() -> None:
    """
    The on_ready is executed AFTER the bot logs in.
    """
    logger.debug("Executing on_ready event.")
    # bot.db.sync()
    logger.info(f'Logged in as {bot.user.name} - ({bot.user.id})')
    connect_to_db(True)
    await load_cogs(bot)


def boink() -> None:
    """
    Loads the bot key as the first arg when running the bot OR from an env variable.
    For example:
        "python __main__.py BOT_TOKEN_HERE"
    """
    if len(sys.argv) > 1:  # Check args for the token first
        token = sys.argv[1].replace('TOKEN=', '')
        logger.debug('Loading Token from arg.')
        bot.run(token)

    elif os.environ['TOKEN'] is not None:  # if not in args, check the env vars
        logger.debug('Loading Token from environment variable.')
        bot.run(os.environ['TOKEN'])

    else:
        logger.critical('You must include a bot token...')
        logger.critical("TOKEN must be in the .env file")
        logger.critical('OR you must run the bot using: "python __main__.py TOKEN=YOUR_DISCORD_TOKEN"')
        return


boink()
