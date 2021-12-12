import discord
from discord.ext import commands
from discord.utils import get

RED = 0xff5677
GREEN = 0x84dfff
YELLOW = 0xFFAFAF

dataMessageID = None

class Ranking(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Exp system
	@commands.Cog.listener()
	async def on_message(self, message):
		