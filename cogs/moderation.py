import discord
from discord.ext import commands
from discord.utils import get
import asyncio

RED = 0xff5677
GREEN = 0x84dfff
YELLOW = 0xFFAFAF

class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.filteredWords = ["nigga"]

	# Ban command
	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def ban(self, ctx, member : discord.Member, *, reason = None):
		username = await self.bot.fetch_user(int(member.id))
		username = username.name

		if reason == None:
			reason = "No reason specified."

		# Send DM
		dm = await member.create_dm()
		embedVar = discord.Embed(title ="You were banned.", description=reason, color=RED)
		await dm.send(embed=embedVar)

		# Ban
		await member.ban(reason = reason)

		# Send Embed
		embedVar = discord.Embed(title = username + " was banned.", description=str(member.id) + ": " + reason, color=GREEN)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.message.channel.send(embed=embedVar)

	# Unban command
	@commands.command()
	@commands.has_permissions(ban_members = True)
	async def unban(self, ctx, id: int, *, reason = None):
		# Unban
		user = await self.bot.fetch_user(id)
		await ctx.guild.unban(user)

		if reason == None:
			reason = "No reason specified."

		# Send embed
		embedVar = discord.Embed(title = user.name + " was unbanned.", description=reason, color=GREEN)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.message.channel.send(embed=embedVar)

	# Mute command
	@commands.command()
	@commands.has_role("Staff")
	async def mute(self, ctx, member:discord.Member, *, reason = None):
		username = await self.bot.fetch_user(int(member.id))
		username = username.name

		if reason == None:
			reason = "No reason specified."

		# Give role
		role = get(member.guild.roles, name="Muted")
		await member.add_roles(role)

		# Send DM
		dm = await member.create_dm()
		embedVar = discord.Embed(title ="You were muted.", description=reason, color=RED)
		await dm.send(embed=embedVar)

	    # Send embed
		embedVar = discord.Embed(title = username + " was muted.", description=str(member.id) + ": " + reason, color=GREEN)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.message.channel.send(embed=embedVar)

	# Unmute command
	@commands.command()
	@commands.has_role("Staff")
	async def unmute(self, ctx, member:discord.Member, *, reason = None):
		username = await self.bot.fetch_user(int(member.id))
		username = username.name

		if reason == None:
			reason = "No reason specified."

		# Give role
		role = get(member.guild.roles, name="Muted")
		await member.remove_roles(role)

		# Send DM
		dm = await member.create_dm()
		embedVar = discord.Embed(title ="You were unmuted.", description=reason, color=GREEN)
		await dm.send(embed=embedVar)

	    # Send embed
		embedVar = discord.Embed(title = username + " was unmuted.", description=str(member.id) + ": " + reason, color=GREEN)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.message.channel.send(embed=embedVar)

	# Purge command
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def purge(self, ctx, limit: int):
		embedVar = discord.Embed(title="Purged " + str(limit) + " messages.", description=" ", color=GREEN)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.message.delete()
		await ctx.channel.purge(limit=limit)
		await ctx.channel.send(embed=embedVar)

	# General on message branch
	@commands.Cog.listener()
	async def on_message(self, message):
		# Filtered words handler
		for word in self.filteredWords:
			if word in message.content:
				await message.delete()

	@commands.command()
	async def ticket(self, ctx):
		category = get(ctx.channel.guild.categories, id=919268015810428958)
		isTicketOpen = False
		alreadyExistingTicket = None

		tempChannel = await ctx.channel.guild.create_text_channel(ctx.message.author.name, category = category)
		for channel in category.channels:
			if channel.name == tempChannel.name and channel != tempChannel:
				isTicketOpen = True
				alreadyExistingTicket = channel
		await tempChannel.delete()

		if isTicketOpen == False:
			overwrites = {
				ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
				ctx.author: discord.PermissionOverwrite(read_messages=True),
				get(ctx.guild.roles, name="Staff"): discord.PermissionOverwrite(read_messages=True)
			}

			channel = await ctx.channel.guild.create_text_channel(ctx.message.author.name, category = category, overwrites = overwrites)

			embedVar = discord.Embed(title = "Ticket created for " + ctx.author.name + ".", description="Head over to " + channel.mention + ".", color=GREEN)
			await ctx.channel.send(embed = embedVar)

			embedVar = discord.Embed(title = "Ticket created.", description="You may talk to an admin or a moderator here.", color=GREEN)
			await channel.send(content = ctx.author.mention, embed = embedVar)
		else:
			embedVar = discord.Embed(title = "A ticket for " + ctx.author.name + " already exists.", description="Head over to " + alreadyExistingTicket.mention + ".", color=YELLOW)
			await ctx.channel.send(embed = embedVar)

			embedVar = discord.Embed(title = "Ticket exists.", description="You may talk to an admin or a moderator here.", color=YELLOW)
			await alreadyExistingTicket.send(content = ctx.author.mention, embed = embedVar)

	@commands.command()
	async def closeticket(self, ctx):
		await ctx.channel.delete()

	# Mod logs
	@commands.Cog.listener()
	async def on_message_edit(self, message_before, message_after):
		embedVar = discord.Embed(title = "Message edited.", description = "Message by " + str(message_before.author.mention) + " edited in " + str(message_before.channel.mention) + ". [Jump to message](https://discord.com/channels/" + str(message_after.channel.guild.id) + "/" + str(message_after.channel.id) + "/" + str(message_after.id) + ")", color=YELLOW)
		embedVar.add_field(name='​From:', value="​" + message_before.content, inline=False)
		embedVar.add_field(name='To:', value="​" + message_after.content, inline=False)
		channel = self.bot.get_channel(833692849689198592)
		await channel.send(embed=embedVar)

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		embedVar = discord.Embed(title = "Message deleted.", description = "Message by " + str(message.author.mention) + " deleted in " + str(message.channel.mention) + ".", color=RED)
		embedVar.add_field(name='Content:', value="​" + message.content, inline=False)
		channel = self.bot.get_channel(833692849689198592)
		await channel.send(embed=embedVar)