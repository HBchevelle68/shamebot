
"""
	This file contains constants and other utilities for robocore
"""

# Discord API imports
from discord import Attachment
from discord.ext.commands import Context


# standard python imports
import time
import datetime
from os import walk
from os.path import abspath, join, dirname 


"""
	**************** Begin globals/exports **************** 
"""

cmdlist = ["$addgif", "$addmeme", "$bugreport", "$gif", "$hello",
		   "$meme", "$ping", "$shamemedaddy", "$version"]

CMD_ADDGIF_HELP    = "Submit gif to gif-pool"
CMD_ADDMEME_HELP   = "Submit meme to meme-pool"
CMD_BUGREPORT_HELP = "Bug report info"
CMD_GIF_HELP       = "Random gif"
CMD_HELLO_HELP     = "Say hello!"
CMD_MEME_HELP      = "Random meme"
CMD_PING_HELP      = "How fast are the bits"
CMD_SHAMEME_HELP   = "Hardcoded shame...for now"
CMD_UPTIME_HELP    = "Get uptime"
CMD_VERSION_HELP   = "Current version"

CMD_ADDGIF_DESC    = "<$addgif> <gif>\nThis only accepts files and will not save links."
CMD_ADDMEME_DESC   = "<$addmeme> <meme>\nThis only accepts files and will not save links."
CMD_BUGREPORT_DESC = "Provides direction for reporting a bug you found"
CMD_GIF_DESC       = "Get random gif from my pool of gifs"
CMD_HELLO_DESC     = "Say hello!"
CMD_MEME_DESC      = "Get random meme from my pool of memes"
CMD_PING_DESC      = "Returns latency"
CMD_SHAMEME_DESC   = "Get a hardcoded shame....for now"
CMD_UPTIME_DESC	   = "Returns uptime of shamebot in the format [D day[s], ][H]H:MM:SS[.UUUUUU]"
CMD_VERSION_DESC   = "Current version"

VERSION = "0.0.50"

BUG = """Found an bug you'd like to report? Go to
https://github.com/HBchevelle68/shamebot/issues
"""

# Provides PWD
PWD = dirname(__name__)

	


"""
	**************** Begin function exports **************** 
"""

"""
	@savememe - wrapper to save a meme submitted to shaebot
"""
async def savememe(Slogger, ctx):
	Slogger.info("Found file attached: %s" % ctx.message.attachments)
	
	#Grab attachment object
	atch = ctx.message.attachments[0]
	fname = atch.filename
	
	#Build out an abs path then save file
	mpool_path = abspath(join(PWD, "images/memes/"))
	byteswritten = await atch.save(join(mpool_path, fname), use_cached=True)
	Slogger.info("saved %s:%d bytes in %s" % (fname, byteswritten, mpool_path))


"""
	@savegif - wrapper to save a gif submitted to shaebot
"""
async def savegif(Slogger, ctx):
	Slogger.info("Found file attached: %s" % ctx.message.attachments)

	#Holy OOP batman
	atch = ctx.message.attachments[0]
	fname = atch.filename

	#Build out an abs path then save file
	gpool_path = abspath(join(PWD, "images/gifs/"))
	byteswritten = await atch.save(join(gpool_path, fname), use_cached=True)
	Slogger.info("saved %s:%d bytes in %s" % (fname, byteswritten, gpool_path))



"""
	@loadimages - only for use during on_ready call
				  loads all memes and gifs. assumes
				  empty pool objects
"""
async def loadimages(Slogger, memepool, gifpool):
	# Populate mempool from disk
	for root, dirs, files in walk(abspath("images/memes/")):
		for file in files:
			if file is None:
				Slogger.error("no memes found!")
				break;
			memepool.append(join(root, file))
			Slogger.info("Loaded meme %s" % memepool[-1]) 

	# Populate gifpool from disk
	for root, dirs, files in walk(abspath("images/gifs/")):
		for file in files:
			if file is None:
				Slogger.error("no gifs found!")
				return
			gifpool.append(join(root, file))
			Slogger.info("Loaded gif %s" % gifpool[-1])



"""
	@reloadmemes - subpiece of loadimages. for use 
				   when meme pool needs to be updated 
"""
async def reloadmemes(Slogger, memepool):
	# Clear list
	memepool.clear()
	Slogger.info("<<CLEARED MEME POOL>>")

	# Populate mempool from disk
	for root, dirs, files in walk(abspath("images/memes/")):
		for file in files:
			if file is None:
				Slogger.error("no memes found!")
				break;
			memepool.append(join(root, file))
			Slogger.info("Loaded meme %s" % memepool[-1])
	Slogger.info("<<RELOADED MEME POOL>>")



"""
	@reloadgifs - subpiece of loadimages. for use 
				  when gif pool needs to be updated 
"""
async def reloadgifs(Slogger, gifpool):
	# Clear list
	gifpool.clear()
	Slogger.info("<<CLEARED GIF POOL>>")
	
	# Populate gifpool from disk
	for root, dirs, files in walk(abspath("images/gifs/")):
		for file in files:
			if file is None:
				Slogger.error("no gifs found!")
				break;
			gifpool.append(join(root, file))
			Slogger.info("Loaded gif %s" % gifpool[-1])
	Slogger.info("<<RELOADED GIF POOL>>")



"""
	@calcuptime - Calculates time difference returns
				  format [D day[s], ][H]H:MM:SS[.UUUUUU]
"""
async def calcuptime(Slogger, stime):
	stime_epoch = time.mktime(stime)
	currtime_epoch = time.mktime(time.localtime())
	return str(datetime.timedelta(seconds=currtime_epoch-stime_epoch)) 
	

