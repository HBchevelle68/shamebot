import traceback
from pprint import pprint
import sys

from utils.colorprint import ColorPrint as CP
from owtests import ow_class_test as OWCT
# Consts

# Print stack trace from called context
def print_strace():
	CP.print_fail("BEGIN Stack Trace")
	traceback.print_exc()
	CP.print_fail("END Stack Trace")



class Core(object):
	# Consts
	SUCCESS = 1
	FAILURE = 0
	RESET = -1
	testTracker = None
	passTracker = None
	failTracker = None
	totalTracker = None
	def __init__(self):
		self.testTracker = self.RESET
		self.passTracker = 0
		self.failTracker = 0
		self.totalTracker = 0
	# Functions to set/reset tracker
	def check_n_set_tracker(self, value):
		if self.testTracker is self.RESET or self.SUCCESS:
			self.testTracker = value

	def reset_tracker(self):
		self.testTracker = self.RESET

	# Setters for trackers
	def inc_fail(self):
		self.failTracker += 1

	def inc_pass(self):
		self.passTracker += 1

	def inc_total(self):
		self.totalTracker += 1
		
	@staticmethod 
	def banner():
		bdr = "="*100
		print()
		CP.print_info(bdr)
		CP.print_info("Testsuite for shamebot 0.0.1", prefix="\t\t\t     ")
		CP.print_info(bdr)

	def show_results(self):
		bdr = "="*100
		print()
		CP.print_info(bdr)
		CP.print_info("Testsuite summary for shamebot 0.0.1", prefix="\t\t\t     ")
		CP.print_info(bdr)
		CP.print_bold("# TOTAL: %d" % self.totalTracker)
		if self.passTracker > 1:
			CP.print_pass("# PASS:  %d" % self.passTracker)
		else:
			CP.print_bold("# PASS:  %d" % self.passTracker)
		if self.failTracker > 1:
			CP.print_fail("# FAIL:  %d" % self.failTracker)
		else:
			CP.print_bold("# FAIL:  %d" % self.failTracker)


