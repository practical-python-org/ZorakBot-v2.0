import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


class CommandSync(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def is_admin(self, ctx) -> bool:
        return ctx.message.author.guild_permissions.administrator

    @commands.command(name="sync")
    @commands.check(is_admin)
    async def sync(self, ctx):
        synced = await self.bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s).")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandSync(bot))