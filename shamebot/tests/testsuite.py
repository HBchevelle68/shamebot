from utils.colorprint import ColorPrint as CP
from owtests import ow_class_test as OWCT
from art import art
from core import core

if __name__ == '__main__':
	tracker = core.TestTracker()
	#art.printart()
	tracker.banner()
	CP.print_warn("Beginning OW Test 1 -- Testing Overwatch constructor", prefix="\n")

	ret = OWCT.OW_Class_test_1(tracker)
	CP.print_warn("End OW Test 1 -- Testing Overwatch constructor", prefix="\n\n")
	if tracker.failCount > 0:
		CP.print_fail("[FAIL] Some or all tests did not pass")

	else:
		CP.print_pass("OW Test 1: [PASS] \tAll Overwatch Class __init__ tests passed")

	tracker.reset()

	tracker.show_results()
