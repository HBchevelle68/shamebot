# Discord API imports
from discord import Attachment
from discord.ext.commands import Context

# Standard python imports
import logging
from os import listdir, walk
from os.path import abspath, join, dirname 





'''
		@RoboMedia - media object to carry around all media used
					 by shamebot in a singluar place. Also provides
					 media access and storage functionality 
'''
class RoboMedia:

	# Public Members
	memepool = list()
	gifpool = list()
	
	# Pseudo Private Members
	_Slogger = None
	_MEMEDIR = abspath(join(dirname(__name__),"images/memes/"))
	_GIFDIR  = abspath(join(dirname(__name__),"images/gifs/"))

	

	""" PUBLIC
		Initialize object by getting a ptr to shamebot's logger
		and performing an Initial load of all media 
	"""
	def __init__(self, corelogger):
		self._Slogger = corelogger
		self._loadmedia()




	""" PUBLIC
		@savememe - wrapper to save a meme submitted to shaebot

	"""
	async def savememe(self, ctx):
		self._Slogger.info("Found file attached: %s" % ctx.message.attachments)
		
		# Grab the first Attachment object's file name
		atch = ctx.message.attachments[0]
		fname = atch.filename

		# Save file to disk 
		byteswritten = await atch.save(join(self._MEMEDIR, fname), use_cached=True)
		self._Slogger.info("saved %s:%d bytes in %s" % (fname, byteswritten, self._MEMEDIR))

		# Append new file to pool in order to incorporate new image 
		self.memepool.append(join(self._MEMEDIR, fname))

		


	""" PUBLIC
		@savegif - wrapper to save a gif submitted to shaebot

	"""
	async def savegif(self, ctx):
		self._Slogger.info("Found file attached: %s" % ctx.message.attachments)

		# Grab the first Attachment object's file name
		atch = ctx.message.attachments[0]
		fname = atch.filename

		# Save file to disk 
		byteswritten = await atch.save(join(self._GIFDIR, fname), use_cached=True)
		self._Slogger.info("saved %s:%d bytes in %s" % (fname, byteswritten, self._GIFDIR))


		# Append new file to pool in order to incorporate new image 
		self.memepool.append(join(self._MEMEDIR, fname))



	"""
		@loadmedia -  Abstraction wrapper to load all media

	"""
	def _loadmedia(self):
		
		# Populate mempool from disk
		self._loadmemes()

		# Populate gifpool from disk
		self._loadgifs()



	"""
		@loadmemes - Core loading function for meme media

	"""
	def _loadmemes(self):
		"""
			Populate mempool from disk
			Make sure its been cleared
		""" 
		self.memepool.clear()
		self.memepool = [join(self._MEMEDIR, file) for file in listdir(self._MEMEDIR)]
		if not self.memepool:
					self._Slogger.error("no memes found!")

		for m in self.memepool:
			self._Slogger.info("Loaded meme %s" % m) 	



	"""
		@loadgifs - Core loading function for gif media

	"""
	def _loadgifs(self):
		"""
			Populate mempool from disk
			Make sure its been cleared
		""" 
		self.gifpool.clear()
		self.gifpool = [join(self._GIFDIR, file) for file in listdir(self._GIFDIR)]
		if not self.gifpool:
					self._Slogger.error("no gifs found!")

		for g in self.gifpool:
			self._Slogger.info("Loaded gif %s" % g) 	




	def listmemes(self):

		if not self.memepool:
			return None


		return [path.split('/')[-1] for path in self.memepool]

	

	def listgifs(self):

		if not self.gifpool:
			return None


		return [path.split('/')[-1] for path in self.gifpool]