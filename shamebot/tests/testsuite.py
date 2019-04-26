from utils.colorprint import ColorPrint as CP
from owtests import ow_class_test as OWCT
from art import art
from core import core

if __name__ == '__main__':
	testCore = core.Core()
	#art.printart()
	testCore.banner()
	CP.print_warn("Beginning OW Test 1 -- Testing Overwatch constructor", prefix="\n")

	ret = OWCT.OW_Class_test_1(testCore)
	CP.print_warn("End OW Test 1 -- Testing Overwatch constructor", prefix="\n\n")
	if testCore.failTracker > 0:
		CP.print_fail("[FAIL] Some or all tests did not pass")

	else:
		CP.print_pass("OW Test 1: [PASS] \tAll Overwatch Class __init__ tests passed")

	testCore.reset_tracker()

	testCore.show_results()
