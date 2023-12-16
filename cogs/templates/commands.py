from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.channel.send("poing")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Ping(bot))

