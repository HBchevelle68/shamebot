# standard python imports
import logging
import os


'''
		@RoboStats - stats object used to track the stats of robocore
'''
class RoboStats:
	# Members
	statsfile = os.path.join(os.path.abspath(os.path.dirname(__name__)), "logs/shamebotStats")
	cmdstats = dict()
	Slogger = None

	def __init__(self, corelogger, cmdlist):
		# verify object
		if corelogger is None:
			print("<<\n ERROR STATS INITIALIZATION FAILED >>\n")
			
		# Grab ptr
		self.Slogger = corelogger

		# Verify object
		if cmdlist is None:
			self.Slogger.error("cmdlist is None")
			
		elif len(cmdlist) == 0:
			self.Slogger.error("cmdlist has 0 elements")
			
		else:
			# Populate cmd list
			for item in cmdlist:
				self.Slogger.info("Setting command usage stat for %s to 0" % item)
				self.cmdstats[str(item)] = 0
		self.Slogger.info("Write all stats to: %s" % (self.statsfile))


	"""
		@logCommandUsage - increments cmd usage counter
	"""
	def logCommandUsage(self, cmd):
		try:
			self.cmdstats[cmd.lower()] += 1
		except KeyError:
			self.Slogger.error("Command <%s> does not exist in stats list. Can't be logged" % cmd.lower())
	
	"""
		@statsToFile - store all stats to log file. Use on clean
	"""
	def statsToFile(self):
		# If either are non existant just leave 
		if self.Slogger is None or len(self.cmdstats) == 0:
			return

		# Record all stats gathered during uptime
		self.Slogger.info("Writing stats to %s" % (self.statsfile)) 
		with open(self.statsfile, 'a') as f:
			for key,value in self.cmdstats.items():
				f.write("%s::%d\n" % (key,value))
			# Write a delimeter marking diff instances
			f.write((('+')*30))