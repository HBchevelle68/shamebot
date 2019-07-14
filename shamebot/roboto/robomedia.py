# Discord API imports
import discord
from discord import Attachment
from discord.ext.commands import Context

# Standard python imports
import random
import logging
import asyncio
from os import listdir, walk
from os.path import abspath, join, dirname, exists 
 
from robostats import RoboStats



'''
		@RoboMedia - media object to carry around all media used
					 by shamebot in a singluar place. Also provides
					 media access and storage functionality 
'''
class RoboMedia:

	# Public Members
	memepool  = list()
	gifpool   = list()
	audiopool = list()
	
	# Pseudo Private Members
	_Slogger  = None
	_MEMEDIR  = abspath(join(dirname(__name__),"images/memes/"))
	_GIFDIR   = abspath(join(dirname(__name__),"images/gifs/"))
	_AUDIODIR = abspath(join(dirname(__name__),"audio/"))
	

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

		while exists(join(self._MEMEDIR, fname)):
			fname_pieces = fname.split('.')
			fname_pieces[0] = fname_pieces[0] + str(random.randint(0,9999999))
			fname = fname_pieces[0] + '.' + fname_pieces[1]

		# Save file to disk 
		byteswritten = await atch.save(join(self._MEMEDIR, fname), use_cached=True)
		self._Slogger.info("saved %s:%d bytes in %s" % (fname, byteswritten, self._MEMEDIR))

		# Append new file to pool in order to incorporate new image 
		self.memepool.append(join(self._MEMEDIR, fname))

				# Provide feedback
		await ctx.send("%s has been added to my meme pool! Thanks! :)" % fname)

		


	""" PUBLIC
		@savegif - wrapper to save a gif submitted to shaebot

	"""
	async def savegif(self, ctx):
		self._Slogger.info("Found file attached: %s" % ctx.message.attachments)

		# Grab the first Attachment object's file name
		atch = ctx.message.attachments[0]
		fname = atch.filename

		while exists(join(self._GIFDIR, fname)):
			fname_pieces = fname.split('.')
			fname_pieces[0] = fname_pieces[0] + str(random.randint(0,9999999))
			fname = fname_pieces[0] + '.' + fname_pieces[1]
                
		# Save file to disk 
		byteswritten = await atch.save(join(self._GIFDIR, fname), use_cached=True)
		self._Slogger.info("saved %s:%d bytes in %s" % (fname, byteswritten, self._GIFDIR))


		# Append new file to pool in order to incorporate new image 
		self.gifpool.append(join(self._GIFDIR, fname))

		# Provide feedback
		await ctx.send("%s has been added to my gif pool! Thanks! :)" % fname)





	""" PUBLIC
		@savegif - wrapper to save a gif submitted to shaebot

	"""
	async def saveaudio(self, ctx):
		self._Slogger.info("Found file attached: %s" % ctx.message.attachments)

		# Grab the first Attachment object's file name
		atch = ctx.message.attachments[0]
		fname = atch.filename

		while exists(join(self._AUDIODIR, fname)):
			fname_pieces = fname.split('.')
			fname_pieces[0] = fname_pieces[0] + str(random.randint(0,9999999))
			fname = fname_pieces[0] + '.' + fname_pieces[1]

		# Save file to disk 
		byteswritten = await atch.save(join(self._AUDIODIR, fname), use_cached=True)
		self._Slogger.info("saved %s:%d bytes in %s" % (fname, byteswritten, self._AUDIODIR))


		# Append new file to pool in order to incorporate new image 
		self.audiopool.append(join(self._AUDIODIR, fname))
		# Provide feedback
		await ctx.send("%s has been added to my audio pool! Thanks! :)" % fname)


	"""
		@loadmedia -  Abstraction wrapper to load all media

	"""
	def _loadmedia(self):
		
		# Populate mempool from disk
		self._loadmemes()

		# Populate gifpool from disk
		self._loadgifs()

		# Populate audiopool from disk
		self._loadaudio()		


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
			Populate gifpool from disk
			Make sure its been cleared
		""" 
		self.gifpool.clear()
		self.gifpool = [join(self._GIFDIR, file) for file in listdir(self._GIFDIR)]
		if not self.gifpool:
					self._Slogger.error("no gifs found!")

		for g in self.gifpool:
			self._Slogger.info("Loaded gif %s" % g) 	




	def _loadaudio(self):
		"""
			Populate audiopool from disk
			Make sure its been cleared
		"""
		self.audiopool.clear()
		self.audiopool = [join(self._AUDIODIR, file) for file in listdir(self._AUDIODIR)]
		if not self.audiopool:
					self._Slogger.error("no audio files found!")

		for mp3 in self.audiopool:
			self._Slogger.info("Loaded audio file %s" % mp3) 





	async def listmemes(self, ctx):

		if not self.memepool:
			return 

		mlist = [path.split('/')[-1] for path in self.memepool]

		async with ctx.typing():
			if mlist != None:
				
				await ctx.send("Here are the Memes you can choose from:")
				msg = ""
				for item in mlist:
					
					msg = msg + item + "\n"  
				await ctx.send(msg)
			
			else:
				await ctx.send("Sorry! Looks like my Meme Pool is empty :(")

	

	async def listgifs(self, ctx):

		if not self.gifpool:
			return
		
		glist = [path.split('/')[-1] for path in self.gifpool]

		async with ctx.typing():
			if glist != None:
				
				await ctx.send("Here are the Gifs you can choose from:")
				msg = ""
				for item in glist:
					
					msg = msg + item + "\n" 
				await ctx.send(msg)
			
			else:
				await ctx.send("Sorry! Looks like my Gif Pool is empty :(")


	async def play_rand_audio(self, Stats, channel):
		# grab the user who sent the command

		if channel != None:
			
			# create StreamPlayer
			vc = await channel.connect()
			f = random.choice(self.audiopool)
			Stats.logAudioUsage(f.split('/')[-1])

			vc.play(discord.FFmpegPCMAudio(f))
			# reduce volume
			vc.source = discord.PCMVolumeTransformer(vc.source)
			vc.source.volume = 0.2
			while vc.is_playing():
				await asyncio.sleep(1)
			# disconnect after the player has finished
			vc.stop()
			await vc.disconnect()
