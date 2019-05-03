# Discord API imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot

# standard python imports
import logging
import traceback
import random
from sys import argv 
from os.path import abspath, join
from logging.handlers import RotatingFileHandler

# internal imports
import roboflame
import roboutils
from robostats import RoboStats


"""
	**************** Begin globals/exports **************** 
"""


# set global Bot object
bot = commands.Bot(command_prefix='$', case_insensitive=True)


""" 
	Attach to discord logger 

"""
DiscordLogPath = abspath(join(roboutils.PWD, "logs/discord.log"))

#Discord logformat is for verbose discord logging that exists in discord module
DiscordlogFormatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

#This splices into the globalized logger object
DISCORDlogger = logging.getLogger('discord')
DISCORDlogger.setLevel(logging.DEBUG)

# Add filehandler 
discordFileHandler = RotatingFileHandler(filename=DiscordLogPath,
										 encoding='utf-8',
										 mode='w',
										 maxBytes=10*1024*1024,
										 backupCount=2)
discordFileHandler.setFormatter(DiscordlogFormatter)
DISCORDlogger.addHandler(discordFileHandler)

"""
	Build Shamebot logger
"""
ShameLogPath   = abspath(join(roboutils.PWD, "logs/shamebot.log"))

#Shameful is our logger, overall less verbose, more focused on server interaction and code stability
ShamefullogFormatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:[%(module)s:%(funcName)s]:  %(message)s')
SHAMElogger = logging.getLogger(__name__)
SHAMElogger.setLevel(logging.DEBUG)

# Add filehandler 
shameFileHandler = RotatingFileHandler(filename=ShameLogPath,
									   encoding='utf-8',
									   mode='a',
									   maxBytes=5*1024,
									   backupCount=2)
shameFileHandler.setFormatter(ShamefullogFormatter)
SHAMElogger.addHandler(shameFileHandler)

# Add Console handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(ShamefullogFormatter)
SHAMElogger.addHandler(consoleHandler)





"""
	**************** Begin shamebot **************** 
"""
memepool = list()
gifpool = list()
statsOBJ = None

"""
	@on_ready() - performed on initialization and login
"""
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

	# Experimental
	for channel in bot.get_all_channels():
		SHAMElogger.info(channel)

	for member in bot.get_all_members():
		SHAMElogger.info(member)

	

"""
	Command handlers

	All commands follow this core layout.
	Each command is logged after it has finished
	all execution required
"""
@bot.command(description=roboutils.CMD_PING_DESC,
			 help=roboutils.CMD_PING_HELP)
async def ping(ctx):
	latency = (bot.latency*1000)
	await ctx.send("%f%s" % (latency, "ms"))
	if latency > 50.0:
		# Shame them
		await ctx.send("Get off the village internet...")
	statsOBJ.logCommandUsage("$ping")


@bot.command(description=roboutils.CMD_MEME_DESC,
			 help=roboutils.CMD_MEME_HELP)
async def meme(ctx):
	await ctx.trigger_typing()
	await ctx.send("", file=discord.File(random.choice(memepool)))
	statsOBJ.logCommandUsage("$meme")


@bot.command(description=roboutils.CMD_GIF_DESC,
			 help=roboutils.CMD_GIF_HELP)
async def gif(ctx):
	await ctx.trigger_typing()
	await ctx.send("", file=discord.File(random.choice(gifpool)))
	statsOBJ.logCommandUsage("$gif")


@bot.command(description=roboutils.CMD_BUGREPORT_DESC,
			 help=roboutils.CMD_BUGREPORT_HELP)
async def bugreport(ctx):
	await ctx.send(roboutils.BUG)
	statsOBJ.logCommandUsage("$bugreport")


@bot.command(description=roboutils.CMD_SHAMEME_DESC,
			 help=roboutils.CMD_SHAMEME_HELP)
async def shamemedaddy(ctx):
	await ctx.send(roboflame.JT)
	statsOBJ.logCommandUsage("$shamemedaddy")


@bot.command(description=roboutils.CMD_HELLO_DESC,
			 help=roboutils.CMD_HELLO_HELP)
async def hello(ctx):
	await ctx.send("Hello %s!" % str(ctx.author).split('#')[0])
	statsOBJ.logCommandUsage("$hello")


@bot.command(description=roboutils.CMD_ADDMEME_DESC,
			 help=roboutils.CMD_ADDMEME_HELP)
async def addmeme(ctx):
	await ctx.trigger_typing()

	if len(ctx.message.attachments) == 1:
		# Pass context to be saved
		await roboutils.savememe(SHAMElogger, ctx)

		# Clear and reload pool; alert user
		await roboutils.reloadmemes(SHAMElogger, memepool)
		await ctx.send("%s has been added to my pool! Thanks! :)" %
			   ctx.message.attachments[0].filename)
		statsOBJ.logCommandUsage("$addmeme")
	else:
		await ctx.send("I can't find an attachment or you passed too many :(")


@bot.command(description=roboutils.CMD_ADDGIF_DESC,
			 help=roboutils.CMD_ADDGIF_HELP)
async def addgif(ctx):
	await ctx.trigger_typing()

	if len(ctx.message.attachments) == 1:
		# Pass context to be saved
		await roboutils.savegif(SHAMElogger, ctx)

		# Clear and reload pool; alert user
		await roboutils.reloadgifs(SHAMElogger, gifpool)
		await ctx.send("%s has been added to my pool! Thanks! :)" %
					   ctx.message.attachments[0].filename)
		statsOBJ.logCommandUsage("$addgif")
	else:
		await ctx.send("I can't find an attachment :(")


@bot.command(description=roboutils.CMD_VERSION_DESC,
			 help=roboutils.CMD_VERSION_HELP)
async def version(ctx):
	await ctx.send("I am currently on %s" % robotils.VERSION)
	statsOBJ.logCommandUsage("$version")



"""
	@on_message() - Core message interaction & response 
"""
@bot.event
async def on_message(message):
	# Shamebot doesn't need to respond to itself :) 
	if message.author == bot.user:
		return

	#Log interaction attempts
	if message.content.startswith('$'):
		SHAMElogger.info("recieved %s from %s" % (message.content, message.author))
	else:
		return

	# Hand off to command handler
	await bot.process_commands(message)

	
"""
	@on_error() - Called when unhandled exception occurs 
"""
@bot.event
async def on_error(event_name, *args, **kwargs):
	SHAMElogger.error("<< BEGIN UNHANDLED EXCEPTION >>")
	SHAMElogger.error("Occured in --> %s" % event_name)
	SHAMElogger.error(traceback.print_exc())
	SHAMElogger.error("<< END UNHANDLED EXCEPTION >>") 


"""
	@on_disconnect() - called on network disconnect, interrupt, etc 
"""
@bot.event
async def on_disconnect():
	SHAMElogger.debug("<< DISCONNECTED >>")
	statsOBJ.statsToFile()


"""
	@on_resume() - called on network re-connect
"""
@bot.event
async def on_resume():
	SHAMElogger.debug("<< RE-CONNECTED >>")


if __name__ == "__main__":
	bot.run(str(argv[1]))