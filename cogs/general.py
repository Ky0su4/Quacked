import discord
from discord.ext import commands
from discord.utils import get

import datetime

import cogs.database as db

from cogs.colors import *

async def send_embed(ctx, embed):
    """
    Function that handles the sending of embeds
    -> Takes context and embed to send
    - tries to send embed in channel
    - tries to send normal message when that fails
    - tries to send embed private with information abot missing permissions
    If this all fails: https://youtu.be/dQw4w9WgXcQ
    """
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)

class General(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		embed = discord.Embed(description=f'**Command Error:**\n{str(error).capitalize()}', color = RED)
		await ctx.send(embed=embed)

	# Ban command
	@commands.command()
	async def ping(self, ctx):
		"""
		Check the bot's latency
		"""
		embedVar = discord.Embed(title = "Ping.", description=str(self.bot.latency) + "s", color=GREEN)
		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.send(embed=embedVar)

	@commands.command()
	async def userinfo(self, ctx, member : discord.Member):
		"""
		Get information about a specific user
		"""
		embedVar = discord.Embed(title=str(member), description="", color=YELLOW)

		embedVar.set_thumbnail(url=member.avatar_url)

		embedVar.add_field(name='ID:', value=member.id, inline=False)
		embedVar.add_field(name='Join date:', value=str(member.joined_at).split(' ')[0], inline=True)
		embedVar.add_field(name='Account creation date:', value=str(member.created_at).split(' ')[0], inline=True)

		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.send(embed=embedVar)

	@commands.command()
	async def help(self, ctx, *input):
		"""
		Sends this help message
		"""
		# !SET THOSE VARIABLES TO MAKE THE COG FUNCTIONAL!
		prefix = "[]" # ENTER YOUR PREFIX - loaded from config, as string or how ever you want!
		version =  "1.0" # enter version of your code
		
		# setting owner name - if you don't wanna be mentioned remove line 49-60 and adjust help text (line 88) 
		owner = 726314967166615592 # ENTER YOU DISCORD-ID
		owner_name = "Duckie#8703" # ENTER YOUR USERNAME#1234

		# checks if cog parameter was given
		# if not: sending all modules and commands not associated with a cog
		if not input:
			# checks if owner is on this server - used to 'tag' owner
			try:
				owner = ctx.guild.get_member(owner).mention

			except AttributeError as e:
				owner = owner

			# starting to build embed
			emb = discord.Embed(title='Commands and modules', color=YELLOW,
								description=f'Use `{prefix}help <module>` to gain more information about that module '
											f'\n')

			# iterating trough cogs, gathering descriptions
			cogs_desc = ''
			for cog in self.bot.cogs:
				cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

			# adding 'list' of cogs to embed
			emb.add_field(name='Modules', value=cogs_desc, inline=False)

			# integrating trough uncategorized commands
			commands_desc = ''
			for command in self.bot.walk_commands():
				# if cog not in a cog
				# listing command if cog name is None and command isn't hidden
				if not command.cog_name and not command.hidden:
					commands_desc += f'{command.name} - {command.help}\n'

			# adding those commands to embed
			if commands_desc:
				emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

			# setting information about author
			emb.add_field(name="About", value=f"The Bots is developed by Duckie#8703, based on discord.py.\n\
									Please visit https://github.com/ducktapeengine/quacked to submit ideas or bugs.")
			emb.set_footer(text="Issued by: " + ctx.author.mention)

		# block called when one cog-name is given
		# trying to find matching cog and it's commands
		elif len(input) == 1:

			# iterating trough cogs
			for cog in self.bot.cogs:
				# check if cog is the matching one
				if cog.lower() == input[0].lower():

					# making title - getting description from doc-string below class
					emb = discord.Embed(title=f'{cog} - Commands', description=self.bot.cogs[cog].__doc__,
										color=YELLOW)

					# getting commands from cog
					for command in self.bot.get_cog(cog).get_commands():
						# if cog is not hidden
						if not command.hidden:
							emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
					# found cog - breaking loop
					break

			# if input not found
			# yes, for-loops have an else statement, it's called when no 'break' was issued
			else:
				emb = discord.Embed(title="What's that?!",
									description=f"I've never heard from a module called `{input[0]}` before",
									color=RED)

		# too many cogs requested - only one at a time allowed
		elif len(input) > 1:
			emb = discord.Embed(title="That's too much.",
								description="Please request only one module at once",
								color=RED)

		# sending reply embed using our own function defined above
		await send_embed(ctx, emb)

	@commands.command()
	async def poll(self, ctx, title:str, *arg):
		"""
		Create a poll
		"""
		return 
		embedVar = discord.Embed(title="Poll", description=title, color=YELLOW)

		# if len(arg) > 

		i = 0
		for opt in arg:
			embedVar.add_field(name="​", value="")
			i = i + 1

		embedVar.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.send(embed=embedVar)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def updaterolelist(self, ctx):
		"""
		Update the role list in <#918732959287214081>
		"""
		embedVar = discord.Embed(title="Reaction Roles", description="React with the respective emotes to get the specific roles.\n🟦 Team Blue\n🟨 Team Yellow\n🟩 Team Green\n🟥 Team Red\n🟪 Team Purple", color=YELLOW)
		
		msg = await ctx.channel.fetch_message(920983341862387744)
		await msg.edit(content="", embed=embedVar)

		await msg.add_reaction("🟦")
		await msg.add_reaction("🟨")
		await msg.add_reaction("🟩")
		await msg.add_reaction("🟥")
		await msg.add_reaction("🟪")

		embedVar = discord.Embed(title="Auto Level Roles", description="These roles will automatically be given to you once you reach the required amount of messages.", color=YELLOW)
		embedVar.add_field(name="Biggest Of Ducks", value="30,000 messages")
		embedVar.add_field(name="Big Duck", value="10,000 messages")
		embedVar.add_field(name="Duck", value="5,000 messages")
		embedVar.add_field(name="Smol Duck", value="2,500 messages")
		
		msg = await ctx.channel.fetch_message(920986374528704532)
		await msg.edit(content="", embed=embedVar)

	@commands.command()
	@commands.has_permissions(administrator = True)
	async def talk(self, ctx, *, content):
		"""
		Make the bot talk
		"""
		await ctx.send(content)
	
	# Reaction roles
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
		user = payload.member

		if message.id != 920983341862387744:
			return

		if user.id == 749996187297251439:
			return
		
		role = get(user.guild.roles, name="Team Blue")
		await user.remove_roles(role)
		role = get(user.guild.roles, name="Team Yellow")
		await user.remove_roles(role)
		role = get(user.guild.roles, name="Team Green")
		await user.remove_roles(role)
		role = get(user.guild.roles, name="Team Red")
		await user.remove_roles(role)
		role = get(user.guild.roles, name="Team Purple")
		await user.remove_roles(role)

		if str(payload.emoji) == "🟦":
			role = get(user.guild.roles, name="Team Blue")
		elif str(payload.emoji) == "🟨":
			role = get(user.guild.roles, name="Team Yellow")
		elif str(payload.emoji) == "🟩":
			role = get(user.guild.roles, name="Team Green")
		elif str(payload.emoji) == "🟥":
			role = get(user.guild.roles, name="Team Red")
		elif str(payload.emoji) == "🟪":
			role = get(user.guild.roles, name="Team Purple")
		await user.add_roles(role)
		await message.remove_reaction(member=user, emoji=payload.emoji)

	# Welcome message
	@commands.Cog.listener()
	async def on_member_join(self, member):
		embedVar = discord.Embed(title = member.name + " joined!", description="Welcome! Feel free to read <#915570583276773436>, hope you have a great stay here. <:DTpepohype:889803114666930186>", color=YELLOW)
		channel = get(member.guild.text_channels, name="introduce-yourself")
		await channel.send(embed=embedVar)
		message = await channel.send(member.mention)
		await message.delete()

	@commands.command()
	async def serverinfo(self, ctx):
		"""
		Get information about this server
		"""
		all_users = []
		for user in ctx.channel.guild.members:
			all_users.append('{}#{}'.format(user.name, user.discriminator))
		all_users.sort()
		all = '\n'.join(all_users)

		channel_count = len([x for x in ctx.channel.guild.channels if type(x) == discord.channel.TextChannel])

		role_count = len(ctx.channel.guild.roles)
		emoji_count = len(ctx.channel.guild.emojis)

		em = discord.Embed(color=0xea7938)
		em.add_field(name='Name', value=ctx.channel.guild.name)
		em.add_field(name='Owner', value=ctx.channel.guild.owner, inline=False)
		em.add_field(name='Members', value=ctx.channel.guild.member_count)
		em.add_field(name='Text Channels', value=str(channel_count))
		em.add_field(name='Number of roles', value=str(role_count))
		em.add_field(name='Number of emotes', value=str(emoji_count))
		em.add_field(name='Created At', value=ctx.channel.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
		em.add_field(name='ID', value=ctx.channel.guild.id)
		em.set_thumbnail(url=ctx.channel.guild.icon_url)
		em.set_footer(text = "Issued by: " + ctx.message.author.name)
		await ctx.send(embed=em)