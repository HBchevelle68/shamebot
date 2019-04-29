
"""
	This file contains constants and other utilities for robocore
"""

# Discord API imports
from discord import Attachment
from discord.ext.commands import Context


# standard python imports
from os import walk
from os.path import abspath, join, dirname 


"""
	**************** Begin globals/exports **************** 
"""

cmdlist = ['$bugreport', '$gif', '$hello', '$meme', '$ping',
 '$shamemedaddy', '$version', '$addmeme'
]

CMD_BUGREPORT_HELP="Bug report info" 
CMD_GIF_HELP="Random gif"
CMD_HELLO_HELP="Say hello!"
CMD_MEME_HELP="Random meme"
CMD_PING_HELP="How fast are the bits"
CMD_SHAMEME_HELP="Hardcoded shame...for now"
CMD_VERSION_HELP="Current version"
CMD_ADDMEME_HELP="Submit meme to memepool"

CMD_BUGREPORT_DESC="Provides direction for reporting a bug you found"
CMD_GIF_DESC="Get random gif from my pool of gifs"
CMD_HELLO_DESC="Say hello!"
CMD_MEME_DESC="Get random meme from my pool of memes"
CMD_PING_DESC="Returns latency"
CMD_SHAMEME_DESC="Get a hardcoded shame....for now"
CMD_VERSION_DESC="Current version"
CMD_ADDMEME_DESC="<$addmeme> <image pasted in discord>"

VERSION="0.0.20"

BUG ="""
Found an bug you'd like to report? Go to
https://github.com/HBchevelle68/shamebot/issues
"""

# Provides PWD
BASEDIR = dirname(__name__)



"""
	**************** Begin function exports **************** 
"""

"""
	@savefile wrapper to save a file submitted to shaebot
"""
async def savefile(Slogger, ctx):
	Slogger.info("Found file attached: %s" % ctx.message.attachments)
	#Holy OOP batman
	atch = ctx.message.attachments[0]
	fname = atch.filename
	#Build out an abs path for reliability
	mpool_path = abspath(join(BASEDIR, "images/memes/"))
	byteswritten = await atch.save(join(mpool_path, fname), use_cached=True)
	Slogger.info("saved %s:%d bytes in %s" % (fname, byteswritten, mpool_path))


"""
	@loadimages only for use during on_ready call
	loads all memes and gifs. assumes empty pool objects
"""	
async def loadimages(Slogger, memepool, gifpool):
	for root, dirs, files in walk(abspath("images/memes/")):
		for file in files:
			if file is None:
				Slogger.error("no memes found!")
				break;
			memepool.append(join(root, file))
			Slogger.info("Loaded meme %s" % memepool[-1]) 

	for root, dirs, files in walk(abspath("images/gifs/")):
		for file in files:
			if file is None:
				Slogger.error("no gifs found!")
				return
			gifpool.append(join(root, file))
			Slogger.info("Loaded gif %s" % memepool[-1])


"""
	@reloadmemes subpiece of loadimages. for use 
	when meme pool needs to be updated 
"""
async def reloadmemes(Slogger, memepool):
	memepool.clear()
	Slogger.info("<<CLEARED MEME POOL>>")
	for root, dirs, files in walk(abspath("images/memes/")):
		for file in files:
			if file is None:
				Slogger.error("no memes found!")
				break;
			memepool.append(join(root, file))
			Slogger.info("Loaded meme %s" % memepool[-1])