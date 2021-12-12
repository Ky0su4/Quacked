import discord
from discord.ext import commands

from cogs.moderation import *
from cogs.general import *
from cogs.ranking import *
from cogs.database import *

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='[]', intents=intents, case_insensitive=True, help_command=None)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

bot.add_cog(Moderation(bot))
bot.add_cog(General(bot))
bot.add_cog(Ranking(bot))
TOKEN = open("token.txt", "r").read()
bot.run(TOKEN)