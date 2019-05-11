# Discord API imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot

# Standard python imports
import logging
import traceback
import time
import random
from sys import argv 
from os.path import abspath, join, dirname
from logging.handlers import RotatingFileHandler

# Internal imports
import roboflame
import roboutils
from robomedia import RoboMedia
from robostats import RoboStats


"""
	**************** Begin globals/exports **************** 
"""


# set global Bot object
bot = commands.Bot(command_prefix='$', case_insensitive=True)


""" 
	Attach to discord logger 

"""
DiscordLogPath = abspath(join(dirname(__name__), "logs/discord.log"))

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
ShameLogPath = abspath(join(dirname(__name__), "logs/shamebot.log"))

#Shameful is our logger, overall less verbose, more focused on server interaction and code stability
ShamefullogFormatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:[%(module)s:%(funcName)s]:  %(message)s')
SHAMElogger = logging.getLogger(__name__)
SHAMElogger.setLevel(logging.DEBUG)

# Add filehandler 
shameFileHandler = RotatingFileHandler(filename=ShameLogPath,
									   encoding='utf-8',
									   mode='a',
									   maxBytes=50*1024*1024,
									   backupCount=4)
shameFileHandler.setFormatter(ShamefullogFormatter)
SHAMElogger.addHandler(shameFileHandler)

# Add Console handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(ShamefullogFormatter)
SHAMElogger.addHandler(consoleHandler)




"""
  Globals used by bot interface. Initialized during on_ready()
  to use Bot execption handler
"""
Stats = None
Media = None

# Grab birthday
starttime = time.localtime()

#Experimental 
channelpool = dict()
userpool = dict()




"""
	**************** Begin shamebot **************** 
"""



"""
	@on_ready() - performed on initialization and login
				  to Discord backend
"""
@bot.event
async def on_ready():
	# Required for write
	global Stats
	global Media

	Stats = RoboStats(SHAMElogger, roboutils.cmdlist)
	Media = RoboMedia(SHAMElogger)

	if len(Stats.cmdstats) == 0:
		SHAMElogger.warning("RoboStats Failed...Continue? (Y/N)")
		if input().lower() == 'n':
			SHAMElogger.warning("Rest in pepes")
			await bot.close()



	# Experimental
	for channel in bot.get_all_channels():
		SHAMElogger.info("%s => %d "% (channel.name, channel.id))
		channelpool[channel.name] = channel.id

	for member in bot.get_all_members():
		SHAMElogger.info(member)
		# Grab Users move into memberpool


	SHAMElogger.info('<< SUCCESSFUL LOGIN {0.user} >>'.format(bot))



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
	Stats.logCommandUsage("$ping")



@bot.command(description=roboutils.CMD_MEME_DESC,
			 help=roboutils.CMD_MEME_HELP)
async def meme(ctx):
	async with ctx.typing():
		await ctx.send("", file=discord.File(random.choice(Media.memepool)))
	Stats.logCommandUsage("$meme")



@bot.command(description=roboutils.CMD_GIF_DESC,
			 help=roboutils.CMD_GIF_HELP)
async def gif(ctx):
	async with ctx.typing():
		await ctx.send("", file=discord.File(random.choice(Media.gifpool)))
	Stats.logCommandUsage("$gif")



@bot.command(description=roboutils.CMD_BUGREPORT_DESC,
			 help=roboutils.CMD_BUGREPORT_HELP)
async def bugreport(ctx):
	await ctx.send(roboutils.BUG)
	Stats.logCommandUsage("$bugreport")



@bot.command(description=roboutils.CMD_SHAMEME_DESC,
			 help=roboutils.CMD_SHAMEME_HELP)
async def shamemedaddy(ctx):
	await ctx.send(roboflame.JT)
	Stats.logCommandUsage("$shamemedaddy")



@bot.command(description=roboutils.CMD_HELLO_DESC,
			 help=roboutils.CMD_HELLO_HELP)
async def hello(ctx):
	await ctx.send("Hello %s!" % str(ctx.author).split('#')[0])
	Stats.logCommandUsage("$hello")



@bot.command(description=roboutils.CMD_ADDMEME_DESC,
			 help=roboutils.CMD_ADDMEME_HELP)
async def addmeme(ctx):
	async with ctx.typing():
		if len(ctx.message.attachments) == 1:
			# Pass context to be saved
			await Media.savememe(ctx)

			# Provide feedback
			await ctx.send("%s has been added to my pool! Thanks! :)" %
				   ctx.message.attachments[0].filename)

			Stats.logCommandUsage("$addmeme")
		else:
			await ctx.send("I can't find an attachment or you passed too many :(")



@bot.command(description=roboutils.CMD_ADDGIF_DESC,
			 help=roboutils.CMD_ADDGIF_HELP)
async def addgif(ctx):
	async with ctx.typing():
		if len(ctx.message.attachments) == 1:
			# Pass context to be saved
			await Media.savegif(ctx)

			# Provide feedback
			await ctx.send("%s has been added to my pool! Thanks! :)" %
						   ctx.message.attachments[0].filename)
			Stats.logCommandUsage("$addgif")
		else:
			await ctx.send("I can't find an attachment or you passed too many :(")



@bot.command(description=roboutils.CMD_VERSION_DESC,
			 help=roboutils.CMD_VERSION_HELP)
async def version(ctx):
	await ctx.send("I am currently on %s" % robotils.VERSION)
	Stats.logCommandUsage("$version")



@bot.command(description=roboutils.CMD_UPTIME_DESC,
			 help=roboutils.CMD_UPTIME_HELP)
async def uptime(ctx):
	async with ctx.typing():
		uptime = await roboutils.calcuptime(SHAMElogger, starttime)
		await ctx.send("%s" % uptime)
	Stats.logCommandUsage("$uptime")



"""
	@on_voice_state_update() - Called whenever a user changes their
							   voice status (join, mute, etc)
"""
@bot.event
async def on_voice_state_update(member, before, after):
	pass
	# TO DO
	# This can be really useful to kick off interesting
	# or funny tasks



"""
	@on_message() - Called when ever a text message is
				    sent in public chats 
"""
@bot.event
async def on_message(message):
	# Shamebot doesn't need to respond to itself :) 
	if message.author == bot.user:
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
	@on_disconnect() - Called on network disconnect, interrupt, etc 
"""
@bot.event
async def on_disconnect():
	SHAMElogger.debug("<< DISCONNECTED >>")
	Stats.statsToFile()



"""
	@on_resume() - called on network re-connect
"""
@bot.event
async def on_resume():
	SHAMElogger.debug("<< RECONNECTED >>")



if __name__ == "__main__":
	bot.run(str(argv[1]))