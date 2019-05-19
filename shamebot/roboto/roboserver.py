# Discord API imports
import discord

# Standard python imports
import logging

class RoboServer:

	userPool = list()
	voiceChannelPool = list()
	textChannelPool  = list()
	voiceUserCount   = dict()

	def __init__(self, vchnl_list, tchnl_list, user_list)