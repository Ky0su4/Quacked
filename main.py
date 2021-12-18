import discord
from discord.ext import commands
import os

from keep_alive import *
keep_alive()

from cogs.moderation import *
from cogs.general import *
from cogs.snowfight import *
from cogs.customcommands import *

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='[]', intents=intents, case_insensitive=True, help_command=None)

# Make sure to set this to True/False depending on if you're running the program on replit or not.
ISONREPLIT = True

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

bot.add_cog(Moderation(bot))
bot.add_cog(General(bot))
bot.add_cog(SnowFight(bot))
bot.add_cog(CustomCommands(bot))

if ISONREPLIT:
	TOKEN = os.getenv("TOKEN")
else:
	TOKEN = open("token.txt", "r").read()
bot.run(TOKEN)