import traceback
from pprint import pprint
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from overwatch import temp
import art
from colorprint import ColorPrint as CP
# Consts
SUCCESS = 1
FAILURE = 0
RESET = -1

# Global return value tracker
testTracker = RESET


# Functions to set/reset tracker
def check_n_set_tracker(value):
	global testTracker
	if testTracker is RESET or SUCCESS:
		testTracker = value

def reset_tracker():
	testTracker = RESET

#Print stack trace from called context
def print_strace():
	CP.print_fail("BEGIN Stack Trace")
	traceback.print_exc()
	CP.print_fail("END Stack Trace")

#Generic Test 1 function
def test_OW_class_init(arg1, arg2):
    test = temp.Overwatch(arg1, arg2)
    print("Battlenet name: " , test.bnet_name)
    print("Hero:            %s " % test.hero)
    print("Hero Value:      %d " % test.hero_val)


def OW_Class_test_1():
	

	try:
		CP.print_info("Test 1.1 -- Overwatch(None, None)", prefix="\n")
		test_OW_class_init(None, None)
		CP.print_fail("[FAIL] Should have thrown --> EmptyAccountStringError....but returned success", prefix="\t\t")
		check_n_set_tracker(FAILURE)
	except Exception as testError:
		if type(testError).__name__ is "EmptyAccountStringError":
			CP.print_pass("[PASS] threw expected EmptyAccountStringError", prefix="\t")
			check_n_set_tracker(SUCCESS)
		else:
			CP.print_fail("[FAIL] Should have thrown --> EmptyAccountStringError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			print_strace()
			check_n_set_tracker(FAILURE)
	
	try:
		CP.print_info("\nTest 1.2 - Overwatch(\"HBchevelle68\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "notachar")
		CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError....but returned success", prefix="\t\t")
		check_n_set_tracker(FAILURE)
	except Exception as testError:
		if type(testError).__name__ is "InvalidHeroNameError":
			CP.print_pass("[PASS] threw expected InvalidHeroNameError", prefix="\t")
			check_n_set_tracker(SUCCESS)
		else:
			CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			print_strace()
			check_n_set_tracker(FAILURE)

	try:
		CP.print_info("\nTest 1.3 - Overwatch(\"HBchevelle68\", None)", prefix="\n")
		test_OW_class_init("HBchevelle68", None)
		CP.print_pass("[PASS] no errors thrown and retrieved ALL HEROES", prefix="\t")
		check_n_set_tracker(SUCCESS)
	except Exception as testError:
		CP.print_fail("[FAIL] Unexpected Error thrown", prefix="\t")
		CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
		print_strace()
		check_n_set_tracker(FAILURE)
		
	try:
		CP.print_info("\nTest 1.4 - Overwatch(\"HBchevelle68\", \"Ana\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "Ana")
		CP.print_pass("[PASS] no errors thrown and retrieved \"Ana\"", prefix="\t")
		check_n_set_tracker(SUCCESS)
	except Exception as testError:
		CP.print_fail("[FAIL] Unexpected Error thrown", prefix="\t")
		CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
		print_strace()
		check_n_set_tracker(FAILURE)

	try:
		CP.print_info("\nTest 1.5 - Overwatch(\"HBchevelle68\", \"Anna\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "Anna")
		CP.print_pass("[PASS] no errors thrown and retrieved \"Ana\"", prefix="\t")
		CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError....but returned success", prefix="\t\t")
		check_n_set_tracker(FAILURE)
	except Exception as testError:
		if type(testError).__name__ is "InvalidHeroNameError":
			CP.print_pass("[PASS] threw expected InvalidHeroNameError", prefix="\t")
			check_n_set_tracker(SUCCESS)
		else:
			CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			print_strace()
			check_n_set_tracker(FAILURE)



if __name__ == '__main__':
	art.printart()
	CP.print_warn("Beginning OW Test 1 -- Testing Overwatch constructor", prefix="\n")

	ret = OW_Class_test_1()
	CP.print_warn("End OW Test 1 -- Testing Overwatch constructor", prefix="\n\n")
	if ret != SUCCESS:
		CP.print_fail("[FAIL] Some or all tests did not pass")

	else:
		CP.print_pass("OW Test 1: [PASS] \tAll Overwatch Class __init__ tests passed")

	reset_tracker()