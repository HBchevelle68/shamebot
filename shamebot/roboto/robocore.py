import discord
from discord.ext import commands
from discord.ext.commands import Bot

import logging
import random
import os
from sys import argv
from logging.handlers import RotatingFileHandler

import roboflame
import roboutils
from robostats import RoboStats

bot = commands.Bot(command_prefix='$', case_insensitive=True)

''' 
	Set up logging 

'''
#Discord logformat is for verbose discord logging that exists in discord module
DiscordlogFormatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

#This splices into the globalized logger object
DISCORDlogger = logging.getLogger('discord')
DISCORDlogger.setLevel(logging.DEBUG)

# Add filehandler 
discordFileHandler = RotatingFileHandler(filename='./logs/discord.log', encoding='utf-8', mode='w', maxBytes=10*1024*1024, backupCount=2)
discordFileHandler.setFormatter(DiscordlogFormatter)
DISCORDlogger.addHandler(discordFileHandler)


#Shameful is our logger, less verbose, more focused on server interaction and code stability
ShamefullogFormatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:[%(module)s:%(funcName)s]:  %(message)s')

SHAMElogger = logging.getLogger(__name__)
SHAMElogger.setLevel(logging.DEBUG)

# Add filehandler 
shameFileHandler = RotatingFileHandler(filename='./logs/shamebot.log', encoding='utf-8', mode='a', maxBytes=5*1024, backupCount=2)
shameFileHandler.setFormatter(ShamefullogFormatter)
SHAMElogger.addHandler(shameFileHandler)

# Add Console handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(ShamefullogFormatter)
SHAMElogger.addHandler(consoleHandler)





'''
	**************** Begin shamebot **************** 
'''
memepool = list()
gifpool = list()
statsOBJ = None

'''
	@on_ready() - performed on initialization and login
'''
@bot.event
async def on_ready():
	global statsOBJ
	#load meme images
	SHAMElogger.info("Loading bot stats trackers")
	statsOBJ = RoboStats(SHAMElogger, roboutils.cmdlist)

	#load memes and gifs
	SHAMElogger.info("Loading memes and gifs")
	await roboutils.loadimages(SHAMElogger, memepool, gifpool)

	#Get command lists
	SHAMElogger.info('<< SUCCESSFUL LOGIN {0.user} >>'.format(bot))

"""
		Command handlers
"""
@bot.command(description=roboutils.CMD_PING_DESC,
			 help=roboutils.CMD_PING_HELP)
async def ping(ctx):
	latency = bot.latency
	await ctx.send("%f%s" % ((latency*1000),'ms'))
	statsOBJ.logCommandUsage(SHAMElogger, '$ping')

@bot.command(description=roboutils.CMD_MEME_DESC,
			 help=roboutils.CMD_MEME_HELP)
async def meme(ctx):
	await ctx.send("", file=discord.File(random.choice(memepool)))
	statsOBJ.logCommandUsage(SHAMElogger, '$meme')

@bot.command(description=roboutils.CMD_GIF_DESC,
			 help=roboutils.CMD_GIF_HELP)
async def gif(ctx):
	await ctx.send("", file=discord.File(random.choice(gifpool)))
	statsOBJ.logCommandUsage(SHAMElogger, '$gif')

@bot.command(description=roboutils.CMD_BUGREPORT_DESC,
			 help=roboutils.CMD_BUGREPORT_HELP)
async def bugreport(ctx):
	await ctx.send(roboutils.BUG)
	statsOBJ.logCommandUsage(SHAMElogger, '$bugreport')

@bot.command(description=roboutils.CMD_SHAMEME_DESC,
			 help=roboutils.CMD_SHAMEME_HELP)
async def shamemedaddy(ctx):
	await ctx.send(roboflame.JT)
	statsOBJ.logCommandUsage(SHAMElogger, '$shamemedaddy')

@bot.command(description=roboutils.CMD_HELLO_DESC,
			 help=roboutils.CMD_HELLO_HELP)
async def hello(ctx):
	await ctx.send('Hello %s!' % str(ctx.author).split('#')[0] )
	statsOBJ.logCommandUsage(SHAMElogger, '$hello')

@bot.command(description=roboutils.CMD_ADDMEME_DESC,
			 help=roboutils.CMD_ADDMEME_HELP)
async def addmeme(ctx):
	if len(ctx.message.attachments) == 1:
		await roboutils.savefile(SHAMElogger, ctx)
		await roboutils.reloadmemes(SHAMElogger, memepool)
		statsOBJ.logCommandUsage(SHAMElogger, '$addmeme')

@bot.command(description=roboutils.CMD_VERSION_DESC,
			 help=roboutils.CMD_VERSION_HELP)
async def version(ctx):
	await ctx.send("I am currently on %s" % roboutils.VERSION)
	statsOBJ.logCommandUsage(SHAMElogger, '$version')



'''
	@on_message() - Core message interaction & response 
'''
@bot.event
async def on_message(message):
	#Log interaction attempts
	if message.content.startswith('$'):
		SHAMElogger.info('recieved %s from %s' % (message.content, message.author))
	else:
		return
	
	# Shamebot doesn't need to respond to itself :) 
	if message.author == bot.user:
		return




	await bot.process_commands(message)

	




'''
	@on_disconnect() - called on network disconnect, interrupt, etc 
'''
@bot.event
async def on_disconnect():
	SHAMElogger.debug('disconnected')
	statsOBJ.statsToFile(SHAMElogger)


#

if __name__ == "__main__":
	#os.path.expanduser('~')
	

	bot.run(str(argv[1]))