import discord
from discord.ext import commands


class MessageListener(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.message) -> None:
        if not message.author.bot:
            print('Message has been sent.')


def setup(bot: commands.Bot) -> None:
    bot.add_cog(MessageListener(bot))
