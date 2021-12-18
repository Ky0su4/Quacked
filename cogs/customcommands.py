import discord
from discord.ext import commands
from discord.utils import get

import cogs.database as db

class CustomCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def addcustomcommand(self, ctx, key, value):
		"""
		Add a new custom command
		"""
		pass
	
	@commands.command()
	async def listcustomcommands(self, ctx):
		"""
		List all the existing custom commands
		"""
		pass

	@commands.command()
	async def removecustomcommand(self, ctx, key):
		"""
		Remove a custom command
		"""
		pass

	@commands.command()
	async def cc(self, ctx, key):
		pass