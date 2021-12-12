import discord
from discord.ext import commands
from discord.utils import get

RED = 0xff5677
GREEN = 0x84dfff
YELLOW = 0xFFAFAF

async def commandhelp(ctx, command, description, sample):
	embedVar = discord.Embed(title=command, description=description, color=YELLOW)
	embedVar.add_field(name='Usage:', value="`[]" + sample + "`", inline=False)
	await ctx.send(embed=embedVar)

class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Ban command
	@commands.command()
	async def ping(self, ctx):
		embedVar = discord.Embed(title = "Ping.", description=str(self.bot.latency) + "s", color=GREEN)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.send(embed=embedVar)


	@commands.command()
	async def help(self, ctx, command=None):
		if command == None:
			embedVar = discord.Embed(title="Help", description="Use =help <command> to get more information on a command.", color=YELLOW)
			embedVar.add_field(name='General', value='ping, help', inline=False)
			embedVar.add_field(name='Moderation', value='ban, unban, mute, unmute, purge, ticket, closeticket​', inline=False)
			embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
			await ctx.send(embed=embedVar)
		else:
			command = command.lower()
			if command == "ping":
				await commandhelp(ctx, command, "Get the bot's latency.", "ping")
			elif command == "help":
				await commandhelp(ctx, command, "Get more information about the various commands.", "help [COMMAND]")
			elif command == "ban":
				await commandhelp(ctx, command, "Ban a member.", "ban @[USER]")
			elif command == "unban":
				await commandhelp(ctx, command, "Unban a member.", "ban [ID]")
			elif command == "mute":
				await commandhelp(ctx, command, "Mute a member.", "mute @[USER]")
			elif command == "unmute":
				await commandhelp(ctx, command, "Unmute a member.", "unmute @[USER]")
			elif command == "purge":
				await commandhelp(ctx, command, "Bulk delete last [N] number of messages.", "purge [N]")
			elif command == "ticket":
				await commandhelp(ctx, command, "Open a Modmail ticket to contact a moderator/admin.", "ticket")
			elif command == "closeticket":
				await commandhelp(ctx, command, "Close a Modmail ticekt.", "closeticket")
			else:
				embedVar = discord.Embed(title="Command doesn't exist.", description="Use =help <command> to get more information on a command.", color=RED)
				embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
				await ctx.send(embed=embedVar)