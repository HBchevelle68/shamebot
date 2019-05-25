# Discord API imports
import discord

# Standard python imports
import logging
import copy

class RoboServer:

	userPool = list()
	voiceChannelPool = list()
	textChannelPool  = list()
	voiceUserCount   = dict()
	_Slogger = None

	def __init__(self, corelogger, vchnl_list, tchnl_list, user_list):
		self._Slogger = corelogger

		# Get a list of all Text Channel Objects 
		self.textChannelPool = tchnl_list

		# Print for logging purposes
		for text in self.textChannelPool:
			self._Slogger.info("Text Channel:%s" % text.name)


		# Get list of all Voice Channel Objects
		self.voiceChannelPool = vchnl_list

		# Iterate, log and populate pool
		for channel in self.voiceChannelPool:
			self._Slogger.info("Voice Channel:%s" % channel)

			# Asseeeeeeeemble base dictionary
			self.voiceUserCount[channel.name] = list()

			# Populate voiceUserCount dictionary
			if len(channel.members) > 0:
				for x in channel.members:
					self._Slogger.info("User in channel: %s" % x.name)
					self.voiceUserCount[channel.name].append(x.name)


		# Get List of users
		self.userPool = user_list


	async def voice_change(self, mbr, before, after):

		print(mbr.name)
		
		if before is None:
			# Virgin join 
			self.voiceUserCount[after].append(mbr.name)
			
		elif after is not None:
			# Remove from old channel
			if(len(self.voiceUserCount[before]) != 0 ):
				self.voiceUserCount[before].remove(mbr.name)
			
			# Add to new channel
			self.voiceUserCount[after].append(mbr.name)
			
			# Check for shaming opportunity
			if len(self.voiceUserCount[after]) == 2:
				return self.voiceUserCount[after]


		return None



