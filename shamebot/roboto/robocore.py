import discord
import logging
import signal
import os
from sys import argv
from logging.handlers import RotatingFileHandler

import roboflame
import roboutils
from robostats import RoboStats


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



def sigint_handler(signum, frame):
    SHAMElogger.info('<CTRL+C>')
    exit()
 
signal.signal(signal.SIGINT, sigint_handler)




'''
	Begin shamebot 
'''
class Shamebot(discord.Client):

	memepool = list()
	statsOBJ = None
	
	'''
		@on_ready() - performed on initialization and login
	'''
	async def on_ready(self):

		#load meme images
		SHAMElogger.info("Loading bot stats trackers")
		self.statsOBJ = RoboStats(SHAMElogger, roboutils.cmdlist)

		#load meme images
		SHAMElogger.info("Loading meme images")
		self.loadmemes()

		#Get command lists
		SHAMElogger.info('Successful login {0.user}'.format(client))

	
	def loadmemes(self):
		for root, dirs, files in os.walk(os.path.abspath("images/memes/")):
			for file in files:
				if file is None:
					SHAMElogger.error("no memes found!")
					return
				self.memepool.append(os.path.join(root, file))
				SHAMElogger.info("Loaded meme %s" % self.memepool[-1]) 


	'''
		@on_message() - Core message interaction & response 
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
		
		elif message.content.startswith('$meme'):
			await message.channel.send("", file=discord.File(self.memepool[0]))

		elif message.content.startswith('$bugreport'):
			await message.channel.send(roboutils.BUG)
		
		elif message.content.startswith('$shamemedaddy'):
			await message.channel.send(roboflame.JT)

		elif message.content.startswith('$hello'):
			await message.channel.send('Hello {.author}!'.format(message))

	'''
		@on_disconnect() - called on network disconnect, interrupt, etc 
	'''
	async def on_disconnect(self):
		SHAMElogger.debug('disconnected')
		self.statsOBJ.statsToFile(SHAMElogger)
	



if __name__ == "__main__":

<<<<<<< HEAD
	client = Shamebot()
	client.run(str(argv[1]))
=======
client = Shamebot()
client.run('LOLOLOL bish pls')
>>>>>>> 8d75bba45e5328e948224859cd83ca9117ca0919
