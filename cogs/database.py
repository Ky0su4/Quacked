from replit import db

import discord
from discord.ext import commands
from discord.utils import get

from cogs.colors import *

async def KeyExists(key):
	key = str(key)
	if key in db.keys():
		return True
	return False

async def CheckAccount(id):
	id = str(id)
	if await KeyExists(id) == False:
		db[id] = 0
	else:
		db[id] = round(db[id])