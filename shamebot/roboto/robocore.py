import discord
import logging
from sys import argv
from logging.handlers import RotatingFileHandler

import roboflame
import roboutils


''' 
	Set up logging 

'''

#Discord logformat is for verbose discord logging that exists in discord module
DiscordlogFormatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

#This splices into the globalized logger object
DISCORDlogger = logging.getLogger('discord')
DISCORDlogger.setLevel(logging.DEBUG)

# Add filehandler 
discordFileHandler = RotatingFileHandler(filename='./logs/discord.log', encoding='utf-8', mode='w', maxBytes=10*1024*1024, backupCount=2)
discordFileHandler.setFormatter(DiscordlogFormatter)
DISCORDlogger.addHandler(discordFileHandler)



#Shameful is our logger, less verbose, more focused on server interaction and code stability
ShamefullogFormatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:[%(module)s:%(funcName)s]:  %(message)s')

SHAMElogger = logging.getLogger(__name__)
SHAMElogger.setLevel(logging.DEBUG)

# Add filehandler 
shameFileHandler = RotatingFileHandler(filename='./logs/shamebot.log', encoding='utf-8', mode='a', maxBytes=5*1024, backupCount=2)
shameFileHandler.setFormatter(ShamefullogFormatter)
SHAMElogger.addHandler(shameFileHandler)

# Add Console handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(ShamefullogFormatter)
SHAMElogger.addHandler(consoleHandler)






'''
	Begin shamebot 
'''
class Shamebot(discord.Client):
	'''
		@on_ready() - performed on initialization and login
	'''
	async def on_ready(self):
		print('Hello! I am logging on discord now!')
		print('I have logged in as {0.user}'.format(client))
		SHAMElogger.info('Successful login {0.user}'.format(client))

	
	'''
		@on_message() - Core message reaction 
	'''
	async def on_message(self, message):
		if message.content.startswith('$'):
			SHAMElogger.info('recieved %s from %s' % (message.content, message.author))
		else:
			return
		
		# Shamebot doesn't need to respond to itself :) 
		if message.author == client.user:
			return

		if message.content.startswith('$help'):
			await message.channel.send(roboutils.helpstr)

		elif message.content.startswith('$hello'):
			await message.channel.send('Hello %s!'% message.author)
    	
		elif message.content.startswith('$shamemedaddy'):
			await message.channel.send(roboflame.JT)



if __name__ == "__main__":
	client = Shamebot()
	client.run(str(argv[1]))