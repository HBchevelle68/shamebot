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

passTracker = 0
failTracker = 0
totalTracker = 0

# Functions to set/reset tracker
def check_n_set_tracker(value):
	global testTracker
	if testTracker is RESET or SUCCESS:
		testTracker = value

def reset_tracker():
	testTracker = RESET

# Setters for trackers
def inc_fail():
	global failTracker
	failTracker += 1

def inc_pass():
	global passTracker
	passTracker += 1

def inc_total():
	global totalTracker
	totalTracker += 1


# Print stack trace from called context
def print_strace():
	CP.print_fail("BEGIN Stack Trace")
	traceback.print_exc()
	CP.print_fail("END Stack Trace")

# Generic Test 1 function
def test_OW_class_init(arg1, arg2):
    test = temp.Overwatch(arg1, arg2)
    print("Battlenet name: " , test.bnet_name)
    print("Hero:            %s " % test.hero)
    print("Hero Value:      %d " % test.hero_val)


def banner():
	bdr = "="*100
	print()
	CP.print_info(bdr)
	CP.print_info("Testsuite for shamebot 0.0.1", prefix="\t\t\t     ")
	CP.print_info(bdr)

def show_results():
	bdr = "="*100
	print()
	CP.print_info(bdr)
	CP.print_info("Testsuite summary for shamebot 0.0.1", prefix="\t\t\t     ")
	CP.print_info(bdr)
	CP.print_bold("# TOTAL: %d" % totalTracker)
	if passTracker > 1:
		CP.print_pass("# PASS:  %d" % passTracker)
	else:
		CP.print_bold("# PASS:  %d" % passTracker)
	if failTracker > 1:
		CP.print_fail("# FAIL:  %d" % failTracker)
	else:
		CP.print_fail("# FAIL:  %d" % failTracker)

def OW_Class_test_1():
	global failTracker
	global passTracker

	try:
		inc_total()
		CP.print_info("Test 1.1 -- Overwatch(None, None)", prefix="\n")
		test_OW_class_init(None, None)
		CP.print_fail("[FAIL] Should have thrown --> EmptyAccountStringError....but returned success", prefix="\t\t")
		check_n_set_tracker(FAILURE)
		inc_fail()
	except Exception as testError:
		if type(testError).__name__ is "EmptyAccountStringError":
			CP.print_pass("[PASS] threw expected EmptyAccountStringError", prefix="\t")
			check_n_set_tracker(SUCCESS)
			inc_pass()
		else:
			CP.print_fail("[FAIL] Should have thrown --> EmptyAccountStringError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			print_strace()
			check_n_set_tracker(FAILURE)
			inc_fail()
	
	try:
		inc_total()
		CP.print_info("\nTest 1.2 - Overwatch(\"HBchevelle68\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "notachar")
		CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError....but returned success", prefix="\t\t")
		check_n_set_tracker(FAILURE)
		inc_fail()
	except Exception as testError:
		if type(testError).__name__ is "InvalidHeroNameError":
			CP.print_pass("[PASS] threw expected InvalidHeroNameError", prefix="\t")
			check_n_set_tracker(SUCCESS)
			inc_pass()
		else:
			CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			print_strace()
			check_n_set_tracker(FAILURE)
			inc_fail()

	try:
		inc_total()
		CP.print_info("\nTest 1.3 - Overwatch(\"HBchevelle68\", None)", prefix="\n")
		test_OW_class_init("HBchevelle68", None)
		CP.print_pass("[PASS] no errors thrown and retrieved ALL HEROES", prefix="\t")
		check_n_set_tracker(SUCCESS)
		inc_pass()
	except Exception as testError:
		CP.print_fail("[FAIL] Unexpected Error thrown", prefix="\t")
		CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
		print_strace()
		check_n_set_tracker(FAILURE)
		inc_fail()
		
	try:
		inc_total()
		CP.print_info("\nTest 1.4 - Overwatch(\"HBchevelle68\", \"Ana\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "Ana")
		CP.print_pass("[PASS] no errors thrown and retrieved \"Ana\"", prefix="\t")
		check_n_set_tracker(SUCCESS)
		inc_pass()
	except Exception as testError:
		CP.print_fail("[FAIL] Unexpected Error thrown", prefix="\t")
		CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
		print_strace()
		check_n_set_tracker(FAILURE)
		inc_fail()

	try:
		inc_total()
		CP.print_info("\nTest 1.5 - Overwatch(\"HBchevelle68\", \"Anna\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "Anna")
		CP.print_pass("[PASS] no errors thrown and retrieved \"Ana\"", prefix="\t")
		CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError....but returned success", prefix="\t\t")
		check_n_set_tracker(FAILURE)
		inc_fail()
	except Exception as testError:
		if type(testError).__name__ is "InvalidHeroNameError":
			CP.print_pass("[PASS] threw expected InvalidHeroNameError", prefix="\t")
			check_n_set_tracker(SUCCESS)
			inc_pass()
		else:
			CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			print_strace()
			check_n_set_tracker(FAILURE)
			inc_fail()



if __name__ == '__main__':
	art.printart()
	banner()
	CP.print_warn("Beginning OW Test 1 -- Testing Overwatch constructor", prefix="\n")

	ret = OW_Class_test_1()
	CP.print_warn("End OW Test 1 -- Testing Overwatch constructor", prefix="\n\n")
	if ret != SUCCESS:
		CP.print_fail("[FAIL] Some or all tests did not pass")

	else:
		CP.print_pass("OW Test 1: [PASS] \tAll Overwatch Class __init__ tests passed")

	reset_tracker()

	show_results()