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
	_Slogger = None

	def __init__(self, corelogger, cmdlist):

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

		# Record all stats gathered during uptime
		self._Slogger.info("Writing stats to %s" % (self.statsfile)) 
		with open(self.statsfile, 'a') as f:
			f.write('\n')
			for key,value in self.cmdstats.items():
				f.write("%s::%d\n" % (key,value))

			# Write a delimeter marking diff instances
			f.write("Total:%d" % self.cmdcount)
			f.write((('+')*30))