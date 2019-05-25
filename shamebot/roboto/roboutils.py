
"""
	This file contains constants and other utilities for robocore
"""

# Standard python imports
import time
import datetime
import logging



"""
	**************** Begin globals/exports **************** 
"""

cmdlist = ["$addgif", "$addmeme", "$bugreport", "$feature", "$gif", "$hello",
		   "$meme", "$ping", "$shamemedaddy", "$uptime", "$version"]

CMD_ADDGIF_HELP     = "Submit gif to gif-pool"
CMD_ADDMEME_HELP    = "Submit meme to meme-pool"
CMD_BUGREPORT_HELP  = "Bug report info"
CMD_FEATUREREQ_HELP = "Make a feature request"
CMD_GIF_HELP        = "Random gif"
CMD_HELLO_HELP      = "Say hello!"
CMD_MEME_HELP       = "Random meme"
CMD_PING_HELP       = "How fast are the bits"
CMD_SHAMEME_HELP    = "Hardcoded shame...for now"
CMD_UPTIME_HELP     = "Get uptime"
CMD_VERSION_HELP    = "Current version"

CMD_ADDGIF_DESC     = "<$addgif> <gif>\nThis only accepts files and will not save links."
CMD_ADDMEME_DESC    = "<$addmeme> <meme>\nThis only accepts files and will not save links."
CMD_BUGREPORT_DESC  = "Provides direction for reporting a bug you found"
CMD_FEATUREREQ_DESC = "To report a bug browse to the link and select New Issue > Feature Request > Get Started"
CMD_GIF_DESC        = "Get random gif from my pool of gifs"
CMD_HELLO_DESC      = "Say hello!"
CMD_MEME_DESC       = "Get random meme from my pool of memes"
CMD_PING_DESC       = "Returns latency"
CMD_SHAMEME_DESC    = "Get a hardcoded shame....for now"
CMD_UPTIME_DESC	    = "Returns uptime of shamebot in the format [D day[s], ][H]H:MM:SS[.UUUUUU]"
CMD_VERSION_DESC    = "Current version"

VERSION = "0.1.0"

BUG = """Found an bug you'd like to report? Go to
https://github.com/HBchevelle68/shamebot/issues
"""

FEATURE = """Have a feature you'd like to see? Go to
https://github.com/HBchevelle68/shamebot/issues
Select New Issue > Feature Request > Get Started
"""
	


"""
	**************** Begin function exports **************** 
"""



"""
	@calcuptime - Calculates time difference returns
				  format [D day[s], ][H]H:MM:SS[.UUUUUU]
"""
async def calcuptime(Slogger, stime):
	# Start time
	stime_epoch = time.mktime(stime)

	# Current time
	currtime_epoch = time.mktime(time.localtime())
	
	# Difference
	return str(datetime.timedelta(seconds=currtime_epoch-stime_epoch)) 
	
