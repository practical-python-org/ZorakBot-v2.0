import os
import discord
from discord.ext import commands, tasks


ZorakV2= os.getenv("TOKEN")
prefix = os.getenv("PREFIX")

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


@bot.event
async def setup_hook() -> None:
    # TODO: Load all cogs in cog folder.
    # await bot.add_cog(Whatever(bot))

@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user.name} - ({bot.user.id})')


bot.run(ZorakV2)
