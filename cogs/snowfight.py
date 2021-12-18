import discord
from discord.ext import commands
from discord.utils import get

import random

import cogs.database as db

from cogs.colors import *

dataMessageID = None

class SnowFight(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# skii, premium, redeem
		
	@commands.command()
	async def collect(self, ctx):
		"""
		Collect a snowball
		"""
		await db.CheckAccount(ctx.author.id)
		
		db.db[str(ctx.author.id)] = db.db[str(ctx.author.id)] + 1
		embedVar = discord.Embed(title="Snowball collected! ☃️", description="You have now " + str(db.db[str(ctx.author.id)]) + " snowball(s). Use []throw to throw it at someone.", color=BLUE)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.message.channel.send(embed=embedVar)

	@commands.command()
	async def throw(self, ctx, member:discord.Member, *, reason=None):
		"""
		Throw a snowball at a user
		"""
		await db.CheckAccount(ctx.author.id)
		await db.CheckAccount(member.id)

		if reason == None:
			reason = ""
		else:
			reason = reason + ". "

		if db.db[str(ctx.author.id)] < 1:
			embedVar = discord.Embed(title="Not enough snowballs.", description="Use []collect to collect more snowballs..", color=BLUE)
			embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
			await ctx.message.channel.send(embed=embedVar)
			return

		db.db[str(ctx.author.id)] = db.db[str(ctx.author.id)] - 1

		if random.uniform(0, 100) < 30:
			embedVar = discord.Embed(title="", description="You missed.", color=BLUE)
			embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
			await ctx.message.channel.send(embed=embedVar)
		else:
			robbedAmount = round(db.db[str(member.id)] * random.uniform(0, 1))
			db.db[str(ctx.author.id)] = db.db[str(ctx.author.id)] + robbedAmount
			db.db[str(member.id)] = db.db[str(member.id)] - robbedAmount
			
			embedVar = discord.Embed(title="", description=str(reason) + member.mention + " got slugged by a snowball.", color=BLUE)
			embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
			await ctx.message.channel.send(embed=embedVar)

	@commands.command()
	async def gamble(self, ctx, num):
		"""
		Do some snowball gambling to gain (or lose) snowballs.
		"""
		await db.CheckAccount(ctx.author.id)

		if db.db[str(ctx.author.id)] < int(num):
			embedVar = discord.Embed(title="Not enough snowballs.", description="Nice try, you can't gamble more snowballs than you already have.", color=BLUE)
			embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
			await ctx.message.channel.send(embed=embedVar)
			return

		# If your dice roll is greater than thw bot's dice roll
		if random.randrange(1, 6) > random.randrange(1, 6):
			db.db[str(ctx.author.id)] = db.db[str(ctx.author.id)] + int(num)

			embedVar = discord.Embed(title="Gamble successful!", description="You now have " + str(db.db[str(ctx.author.id)]) + " snowballs.", color=BLUE)
			embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
			await ctx.message.channel.send(embed=embedVar)
		else:
			db.db[str(ctx.author.id)] = db.db[str(ctx.author.id)] - int(num)

			embedVar = discord.Embed(title="Gamble failed.", description="You now have " + str(db.db[str(ctx.author.id)]) + " snowballs.", color=BLUE)
			embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
			await ctx.message.channel.send(embed=embedVar)
	
	@commands.command()
	async def share(self, ctx, member:discord.Member, num):
		"""
		Sharing is caring! Share your snowballs with someone else
		"""
		await db.CheckAccount(ctx.author.id)
		await db.CheckAccount(member.id)

		if db.db[str(ctx.author.id)] < int(num):
			embedVar = discord.Embed(title="Not enough snowballs.", description="Nice try, you can't share more snowballs than you already have.", color=BLUE)
			embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
			await ctx.message.channel.send(embed=embedVar)
			return

		db.db[str(ctx.author.id)] = db.db[str(ctx.author.id)] - int(num)
		db.db[str(member.id)] = db.db[str(member.id)] + int(num)

		embedVar = discord.Embed(title="Shared " + num + " snowballs.", description=member.mention + " now has " + db.db[str(member.id)] + " snowballs.", color=BLUE)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.message.channel.send(embed=embedVar)

	@commands.command()
	async def balance(self, ctx, member:discord.Member=None):
		"""
		Check your balance
		"""
		if member == None:
			member = ctx.author

		await db.CheckAccount(member.id)

		embedVar = discord.Embed(title=member.name + " has " + str(db.db[str(member.id)]) + " snowballs.", description="Use []collect to collect more snowballs.", color=BLUE)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.message.channel.send(embed=embedVar)