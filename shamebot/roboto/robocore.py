# Discord API imports
import discord
from discord import ChannelType
from discord.ext import commands
from discord.ext.commands import Bot


# Standard python imports
import logging
import traceback
import time
import random
import asyncio
from sys import argv 
from os.path import abspath, join, dirname
from logging.handlers import RotatingFileHandler


# Internal imports
import roboflame
import roboutils
from robomedia import RoboMedia
from robostats import RoboStats
from roboserver import RoboServer


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
# Global robo* Objects
Stats = None
Media = None
Server = None

# Init birthday
starttime = time.localtime()

MASTER = "HBchevelle68"

"""
	**************** Begin shamebot **************** 






	Command handlers

	All commands follow this core layout. Each command is logged after
	it has finished execution

	
	General design of commands is to kick off some form task for the
	user. These tasks often will return some form of feedback to 
	the user either in the form of media or text based response


	Commands cannot be accessed interanlly, meaning, you cannot trigger
	a task from within an event or Robo* class. However, nearly all 
	functionality within commands are accessiable from outside 
	the commands and if need can be accessed 

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





@bot.command(description=roboutils.CMD_ADDMEME_DESC,
			 help=roboutils.CMD_ADDMEME_HELP)
async def addmeme(ctx):
	async with ctx.typing():
		if len(ctx.message.attachments) == 1:
			# Pass context to be saved
			await Media.savememe(ctx)

			# Provide feedback
			await ctx.send("%s has been added to my meme pool! Thanks! :)" %
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
			await ctx.send("%s has been added to my gif pool! Thanks! :)" %
						   ctx.message.attachments[0].filename)
			Stats.logCommandUsage("$addgif")
		else:
			await ctx.send("I can't find an attachment or you passed too many :(")


@bot.command(description=roboutils.CMD_ADDGIF_DESC,
			 help=roboutils.CMD_ADDGIF_HELP)
async def addaudio(ctx):
	async with ctx.typing():
		if len(ctx.message.attachments) == 1:
			# Pass context to be saved
			await Media.saveaudio(ctx)

			# Provide feedback
			await ctx.send("%s has been added to my audio pool! Thanks! :)" %
						   ctx.message.attachments[0].filename)
			Stats.logCommandUsage("$addgif")
		else:
			await ctx.send("I can't find an attachment or you passed too many :(")


@bot.command(description=roboutils.CMD_LISTMEMES_DESC,
			 help=roboutils.CMD_LISTMEMES_HELP)
async def listmemes(ctx):
	
	await Media.listmemes(ctx)

	Stats.logCommandUsage("$listmemes")





@bot.command(description=roboutils.CMD_LISTGIFS_DESC,
			 help=roboutils.CMD_LISTGIFS_HELP)
async def listgifs(ctx):
	
	await Media.listgifs(ctx)
	
	Stats.logCommandUsage("$listgifs")





@bot.command(description=roboutils.CMD_BUGREPORT_DESC,
			 help=roboutils.CMD_BUGREPORT_HELP)
async def bugreport(ctx):

	await ctx.send(roboutils.BUG)

	Stats.logCommandUsage("$bugreport")





@bot.command(description=roboutils.CMD_SHAMEME_DESC,
			 help=roboutils.CMD_SHAMEME_HELP)
async def shamemedaddy(ctx):
	
	temp = [ctx.author.name]

	async with ctx.typing():

		# Make sure we haven't recently flamed 
		if await Server.check_user_cooldown(temp):
			
			await ctx.send(roboflame.JT)
			
			# Set flame cooldown
			await Server.init_user_cooldown(temp)

		else:
			
			await ctx.send("But I already flamed that boi...")

	Stats.logCommandUsage("$shamemedaddy")





@bot.command(description=roboutils.CMD_HELLO_DESC,
			 help=roboutils.CMD_HELLO_HELP)
async def hello(ctx):

	await ctx.send("Hello %s!" % str(ctx.author).split('#')[0])

	Stats.logCommandUsage("$hello")





@bot.command(description=roboutils.CMD_VERSION_DESC,
			 help=roboutils.CMD_VERSION_HELP)
async def version(ctx):

	await ctx.send("I am currently on %s" % roboutils.VERSION)

	Stats.logCommandUsage("$version")





@bot.command(description=roboutils.CMD_UPTIME_DESC,
			 help=roboutils.CMD_UPTIME_HELP)
async def uptime(ctx):

	async with ctx.typing():

		uptime = await roboutils.calcuptime(SHAMElogger, starttime)
		await ctx.send("%s" % uptime)

	Stats.logCommandUsage("$uptime")





@bot.command(description=roboutils.CMD_FEATUREREQ_DESC,
			 help=roboutils.CMD_FEATUREREQ_HELP)
async def feature(ctx):

	async with ctx.typing():
		await ctx.send("%s" % roboutils.FEATURE)

	Stats.logCommandUsage("$feature")




@bot.command(description=roboutils.CMD_FEATUREREQ_DESC,
			 help=roboutils.CMD_FEATUREREQ_HELP)
async def dev(ctx):

	if ctx.author.name == MASTER: 
		await bot.logout()

	else:
		async with ctx.typing():
			await ctx.send("%s kys" % ctx.author.name)


@bot.command(description=roboutils.CMD_VOICE_DESC,
			 help=roboutils.CMD_VOICE_HELP)
async def voice(ctx):
	# grab the user who sent the command
	author = ctx.message.author
	channel = author.voice.channel
	if channel != None:
		# create StreamPlayer
		vc = await channel.connect()
		vc.play(discord.FFmpegPCMAudio(random.choice(Media.audiopool)), after=lambda: print('done'))

		while vc.is_playing():
		    await asyncio.sleep(1)
		# disconnect after the player has finished
		vc.stop()
		await vc.disconnect()

	Stats.logCommandUsage("$voice")

"""

	Events

	Events are the actions or incidents we ask shame bot to 
	trigger on and will always occur prior to commands. 

	

	Unlike commands, which are generally self explanitory and are 
	inteded to be exposed mainly to the user, events are intended 
	to be shamebot driven. This is because Users have no 
	visability into events and nor should they. Events are for 
	specialty cases where shamebot needs to execute specifc logic
	due to a triggering "event" :)


	Events should have full function documentation where as commands
	due to their design as being entry points into shamebot functionality
	are not required to be fully documented 

"""


"""
	@on_ready() - performed on initialization and login
				  to Discord backend
"""
@bot.event
async def on_ready():
	# Required for global write
	global Stats
	global Media
	global Server

	
	# Create global stats object
	Stats = RoboStats(SHAMElogger, roboutils.cmdlist)
	
	# Verify stats setup correctly 
	if len(Stats.cmdstats) == 0:
		SHAMElogger.warning("RoboStats Failed...Continue? (Y/N)")
		if input().lower() == 'n':
			SHAMElogger.warning("Rest in pepes")
			await bot.close()

	# Create global media object 
	Media = RoboMedia(SHAMElogger)

	Server = RoboServer(SHAMElogger,
						bot.guilds[0].voice_channels,
						bot.guilds[0].text_channels,
						bot.get_all_members())


	SHAMElogger.info('<< SUCCESSFUL LOGIN {0.user} >>'.format(bot))





"""
	@on_voice_state_update() - Called whenever a user changes their
							   voice status (join, mute, etc)
"""
@bot.event
async def on_voice_state_update(member, before, after):
	if member.name != "shamebot":
		# Set some variables up to the info we need
		if before.channel != None:
			bchnl_name = before.channel.name
		else:
			bchnl_name = None
		if after.channel != None:
			achnl_name = after.channel.name
			await Media.play_rand_audio(after.channel)
		else:
			achnl_name  = None 

		# Register change
		ret = await Server.voice_change(member, bchnl_name, achnl_name) 
		

		# Make sure we haven't recently flamed 
		if ret != None and await Server.check_user_cooldown(ret):

			async with Server.textChannelPool[0].typing():
				await Server.textChannelPool[0].send("BOIS")
				await Server.textChannelPool[0].send("%s and %s are about to YeeeeEEEEEeeeeeEEEEEeeEEeEEEeeet" % (ret[0], ret[1]))

			# Set flame cooldown
			await Server.init_user_cooldown(ret)

		# DEBUGGING
		SHAMElogger.info("%s: %s -> %s" % (member.name, bchnl_name, achnl_name))





"""
	@on_message() - Called when ever a text message is
				    sent in public chats 
"""
@bot.event
async def on_message(message):
	# Shamebot doesn't need to respond to itself :) 
	if message.author != bot.user:
		# Hand off to command handler
		await bot.process_commands(message)

	


	
@bot.event
async def on_guild_channel_create(channel):
	SHAMElogger.info("New channel created")

	await Server.new_channel(channel)


@bot.event
async def on_guild_channel_delete(channel):
	SHAMElogger.info("Channel delete")

	await Server.del_channel(channel)

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
	@on_disconnect() - Called on network disconnect 
"""
@bot.event
async def on_disconnect():
	SHAMElogger.warning("<< DISCONNECTED >>")





"""
	@on_resume() - called on network re-connect
"""
@bot.event
async def on_resume():
	global Stats
	SHAMElogger.warning("<< RECONNECTED >>")
	if Stats == None:
		Stats = RoboStats(SHAMElogger, roboutils.cmdlist)




if __name__ == "__main__":

		
	bot.run(str(argv[1]))

	SHAMElogger.warning("<< IM DYING LOLOLOL >>")
	if Stats != None:
		Stats.statsToFile()
		


	

	
