import sys
import traceback
from utils.colorprint import ColorPrint as CP

# Print stack trace from called context
def print_strace():
	CP.print_fail("BEGIN Stack Trace")
	traceback.print_exc()
	CP.print_fail("END Stack Trace")


class TestTracker(object):
	# Consts
	SUCCESS = 1
	FAILURE = 0
	RESET = -1
	

	def __init__(self):
		self.reset()


	def reset(self):
		self.passCount = 0
		self.failCount = 0
		self.totalCount = 0


	def inc_fail(self):
		self.failCount += 1
		self._inc_total()


	def inc_pass(self):
		self.passCount += 1
		self._inc_total()


	def _inc_total(self):
		self.totalCount += 1


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
		CP.print_bold("# TOTAL: %d" % self.totalCount)
		if self.passCount > 0:
			CP.print_pass("# PASS:  %d" % self.passCount)
		else:
			CP.print_bold("# PASS:  %d" % self.passCount)
		if self.failCount > 0:
			CP.print_fail("# FAIL:  %d" % self.failCount)
		else:
			CP.print_bold("# FAIL:  %d" % self.failCount)


