import logging
import discord
from discord.ext import commands


logger = logging.getLogger(__name__)


class MessagePoints(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    """
    Adding and removing members from the DB
    """
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """When a member joins, add them to the DB."""
        self.bot.db.add_member_to_points_table(member, member.guild.id, member.id)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):  # pylint: disable=E1101
        """When a member leaves, remove them from the DB."""
        self.bot.db.delete_member_from_points_table(member.guild.id, member.id)

    """
    On_message events
    """
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """When a member sends a message, give them points."""
        if message.author.bot:
            return
        message_value = len(message.content.split(" "))
        self.bot.db.add_points(message.author.id, abs(message_value))

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """When a member deletes a message, remove points."""
        message_value = len(message.content.split(" "))
        self.bot.db.remove_points(message.author.id, abs(message_value))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MessagePoints(bot))
