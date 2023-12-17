from discord.ext import commands
from logger import *


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        log_debug("Ping command used.")
        await ctx.channel.send("poing")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))

