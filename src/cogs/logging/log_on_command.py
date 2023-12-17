import logging
from discord.ext import commands


logger = logging.getLogger(__name__)


class CommandListener(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name='on_command')
    async def log_commands(self, ctx):
        logger.info(f'{ctx.guild.name} -- {ctx.author} -- Used {ctx.command}')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(CommandListener(bot))
