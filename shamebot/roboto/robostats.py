import logging
import os

'''
		@RoboStats: stats object used to track the stats of robocore
'''
class RoboStats:
	statsfile = os.path.join(os.path.abspath(os.path.dirname(__name__)), "logs/shamebotStats")
	cmdstats = dict()

	def __init__(self, Slogger, cmdlist):
		if cmdlist is None:
			Slogger.error("cmdlist is None")
			return
		elif len(cmdlist) == 0:
			Slogger.error("cmdlist has 0 elements")
			return
		else:
			for item in cmdlist:
				Slogger.info("Setting command usage stat for %s to 0" % item)
				self.cmdstats[str(item)] = 0
		Slogger.info("All stats set to be written to %s" % (self.statsfile))

	def logCommandUsage(self, Slogger, cmd):
		try:
			self.cmdstats[cmd.lower()] += 1
		except KeyError:
			Slogger.error("Command <%s> does not exist and cannot be logged" % cmd.lower())

	def statsToFile(self, Slogger):
		Slogger.info("Writing stats to %s"% (self.statsfile)) 
		with open(self.statsfile, "a") as f:
			for key,value in self.cmdstats.items():
				f.write("%s::%d\n" % (key,value))
			f.write("++++++++++")