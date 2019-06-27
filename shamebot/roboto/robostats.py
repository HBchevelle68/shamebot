# Discord API imports
import discord
from discord import Attachment
from discord.ext.commands import Context

# standard python imports
import logging
import os


'''
		@RoboStats - stats object used to track the stats of robocore
'''
class RoboStats:
	# Members
	statsfile = os.path.join(os.path.abspath(os.path.dirname(__name__)), "logs/shamebotStats")
	cmdcount = None 
	cmdstats = dict()
	audiostats = dict()
	memestats = dict()
	gifstats = dict()

	# Pseudo Private Members
	_Slogger = None

	def __init__(self, corelogger, cmdlist, mediadict):

		# Grab ptr
		self._Slogger = corelogger

		self.cmdcount = 0

		# Verify object
		if cmdlist is None or len(cmdlist) == 0:
			self._Slogger.error("Error loading cmdlist ")
			
		else:
			# Populate cmd list
			for item in cmdlist:
				self._Slogger.info("Setting command usage stat for %s to 0" % item)
				self.cmdstats[str(item)] = 0

		self._Slogger.info("Write all stats to: %s" % (self.statsfile))

		self._initMediaStats(mediadict)

	def _initMediaStats(self, mediadict):
		tempAudioList = mediadict["audio"]
		tempMemeList = mediadict["meme"]
		tempGifList = mediadict["gif"]

		for item in tempAudioList:
			self._Slogger.info("Setting audio usage stat for %s to 0" % item)
			self.audiostats[str(item)] = 0
			

		for item in tempMemeList:
			self._Slogger.info("Setting meme usage stat for %s to 0" % item)
			self.memestats[str(item)] = 0
		

		for item in tempGifList:
			self._Slogger.info("Setting gif usage stat for %s to 0" % item)
			self.gifstats[str(item)] = 0
	




	def logAudioUsage(self, fileused):
		
		if fileused in self.audiostats:
			self.audiostats[fileused] += 1 
			self._Slogger.info("Gave %s" % fileused)

	def logMemeUsage(self, fileused):
		
		if fileused in self.memestats:
			self.memestats[fileused] += 1 
			self._Slogger.info("Gave %s" % fileused)

	def logGifUsage(self, fileused):
		
		if fileused in self.gifstats:
			self.gifstats[fileused] += 1 
			self._Slogger.info("Gave %s" % fileused)

	async def displayStats(self, ctx):

		async with ctx.typing():
			if self.audiostats.items() != None:
				
				await ctx.send("All Stats:")
				msg = ""
				for item, num in self.audiostats.items():
					msg = msg + item + " = " + str(num) + "\n"

				msg = msg + "\n\n"
				for item, num in self.memestats.items():
					msg = msg + item + " = " + str(num) + "\n"
				
				msg = msg + "\n\n"
				for item, num in self.gifstats.items():
					msg = msg + item + " = " + str(num) + "\n"
				await ctx.send(msg)
			
			else:
				await ctx.send("INCREASE MASS AND BLOW THE ASS I HAVE NO STATS!")


	"""
		@logCommandUsage - increments cmd usage counter
	"""
	def logCommandUsage(self, cmd):
		try:

			self._Slogger.info("Executed command %s" % cmd)

			self.cmdstats[cmd.lower()] += 1
			
			self.cmdcount += 1

		except KeyError:
			self._Slogger.error("Command <%s> does not exist in stats list. Can't be logged" % cmd.lower())
	
	"""
		@statsToFile - store all stats to log file. Use on clean
	"""
	def statsToFile(self):
		# If either are non existant just leave 
		if self._Slogger is None or len(self.cmdstats) == 0:
			return


		self._Slogger.info("Writing stats to %s" % (self.statsfile)) 
		
		# Record all stats gathered during uptime
		with open(self.statsfile, 'a') as f:
			
			f.write('\n')
			
			# Record each piece of data
			for key,value in self.cmdstats.items():
				f.write("%s::%d\n" % (key,value))

			# Write a delimeter marking diff instances
			f.write("Total:%d" % self.cmdcount)
			f.write((('+')*30))