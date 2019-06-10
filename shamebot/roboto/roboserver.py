# Discord API imports
import discord


# Standard python imports
import logging
import time


class RoboServer():

	# Public Members
	userPool 		 = list()
	voiceChannelPool = list()
	textChannelPool  = list()
	voiceUserCount   = dict()

	# Pseudo Private Members
	_userCooldowns	 = dict()
	_base_cd_time	 = 30 
	_Slogger 	 	 = None



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
			if channel.members:
				for x in channel.members:
					self._Slogger.info("User in channel: %s" % x.name)
					self.voiceUserCount[channel.name].append(x.name)


		# Get List of users
		self.userPool = user_list
		for u in self.userPool:
			self._userCooldowns[u.name] = 0
			self._Slogger.info("User: %s" % u)
			print(type(u))
			print(type(u.name))
			
		for u, cd in self._userCooldowns.items():
			self._Slogger.debug("User:Cooldown --> %s:%d" % (u, cd))



	async def voice_change(self, mbr, before, after):

				
		if before == None and after != None:
			# Virgin join 
			self.voiceUserCount[after].append(mbr.name)
		

		elif before != None and after == None:
			# Remove from old channel
			if self.voiceUserCount[before]:
				self.voiceUserCount[before].remove(mbr.name) 


		elif after != None and before != None:
			# Remove from old channel
			if self.voiceUserCount[before]:
				self.voiceUserCount[before].remove(mbr.name)
			
			# Add to new channel
			self.voiceUserCount[after].append(mbr.name)
		

		else:
			self._Slogger.error("Before and after == None")



		# Check for shaming opportunity
		if after != None and len(self.voiceUserCount[after]) == 2:
			return self.voiceUserCount[after]


		return None





	async def new_channel(self, channel):
		
		if isinstance(channel, discord.channel.TextChannel):

			# Add to text pool 
			self.textChannelPool.append(channel)
			
			self._Slogger.info("Adding %s to textChannelPool" % channel)

		elif isinstance(channel, discord.channel.VoiceChannel):

			# Add to voice pool and voice user count
			self.voiceChannelPool.append(channel)
			self.voiceUserCount[channel.name] = list()

			self._Slogger.info("Adding %s to voiceChannelPool &&  voiceUserCount" % channel)





	async def del_channel(self, channel):

		if isinstance(channel, discord.channel.TextChannel):

			# Remove from text pool 
			self.textChannelPool.remove(channel)
			
			self._Slogger.info("Removing %s from textChannelPool" % channel)

		elif isinstance(channel, discord.channel.VoiceChannel):

			# Remove from voice pool and voice user count
			self.voiceChannelPool.remove(channel)
			del self.voiceUserCount[channel.name]
			
			self._Slogger.info("Removing %s from voiceChannelPool and voiceUserCount" % channel)


	"""
		Kick off cooldown timer(s) for shame. Takes one param which
		is the list of users that have been shamed

		items in list must be discord.member.Member.name (str)
	"""
	async def init_user_cooldown(self, user_list):
		
		for u in user_list:
			if isinstance(u, str):
				self._userCooldowns[u] = time.time()
				self._Slogger.info("Setting cooldown timer for %s" % u)
			else:
				self._Slogger.error("userlist item incorrect type")
				


	async def check_user_cooldown(self, user_list):
		
		
		for u in user_list:

			# Verify type  
			if isinstance(u, str):

				# If the user has never had a cooldown started flame that hoe
				if self._userCooldowns[u] == 0 :
					continue

				# Get time difference between now when timer was kicked off
				epoch_diff = (time.time() - self._userCooldowns[u])
				
				if epoch_diff < self._base_cd_time :

					# Too soon
					return False
			
			else:
				self._Slogger.error("targeted_user incorrect type")

		return True