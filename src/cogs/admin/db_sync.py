import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class DBsync(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def db_sync(self, guilds=True, channels=True, members=True, roles=True, settings=True) -> None:
        logger.debug("db_sync command used.")
        self.bot.db.sync(self, guilds=True, channels=True, members=True, roles=True, settings=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DBsync(bot))

