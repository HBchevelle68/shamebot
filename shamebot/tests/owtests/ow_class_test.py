import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from overwatch import temp

from core import core
from utils.colorprint import ColorPrint as CP

# Consts
SUCCESS = 1
FAILURE = 0

# Generic Test 1 function
def test_OW_class_init(arg1, arg2):
    test = temp.Overwatch(arg1, arg2)
    print("Battlenet name: " , test.bnet_name)
    print("Hero:            %s " % test.hero)
    print("Hero Value:      %d " % test.hero_val)


def OW_Class_test_1(coreObj):


	try:
		coreObj.inc_total()
		CP.print_info("Test 1.1 -- Overwatch(None, None)", prefix="\n")
		test_OW_class_init(None, None)
		CP.print_fail("[FAIL] Should have thrown --> EmptyAccountStringError....but returned success", prefix="\t\t")
		coreObj.check_n_set_tracker(coreObj.FAILURE)
		coreObj.inc_fail()
	except Exception as testError:
		if type(testError).__name__ is "EmptyAccountStringError":
			CP.print_pass("[PASS] threw expected EmptyAccountStringError", prefix="\t")
			coreObj.check_n_set_tracker(coreObj.SUCCESS)
			coreObj.inc_pass()
		else:
			CP.print_fail("[FAIL] Should have thrown --> EmptyAccountStringError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			core.print_strace()
			coreObj.check_n_set_tracker(coreObj.FAILURE)
			coreObj.inc_fail()
	
	try:
		coreObj.inc_total()
		CP.print_info("\nTest 1.2 - Overwatch(\"HBchevelle68\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "notachar")
		CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError....but returned success", prefix="\t\t")
		coreObj.check_n_set_tracker(coreObj.FAILURE)
		coreObj.inc_fail()
	except Exception as testError:
		if type(testError).__name__ is "InvalidHeroNameError":
			CP.print_pass("[PASS] threw expected InvalidHeroNameError", prefix="\t")
			coreObj.check_n_set_tracker(coreObj.SUCCESS)
			coreObj.inc_pass()
		else:
			CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			core.print_strace()
			coreObj.check_n_set_tracker(coreObj.FAILURE)
			coreObj.inc_fail()

	try:
		coreObj.inc_total()
		CP.print_info("\nTest 1.3 - Overwatch(\"HBchevelle68\", None)", prefix="\n")
		test_OW_class_init("HBchevelle68", None)
		CP.print_pass("[PASS] no errors thrown and retrieved ALL HEROES", prefix="\t")
		coreObj.check_n_set_tracker(coreObj.SUCCESS)
		coreObj.inc_pass()
	except Exception as testError:
		CP.print_fail("[FAIL] Unexpected Error thrown", prefix="\t")
		CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
		core.print_strace()
		coreObj.check_n_set_tracker(coreObj.FAILURE)
		coreObj.inc_fail()
		
	try:
		coreObj.inc_total()
		CP.print_info("\nTest 1.4 - Overwatch(\"HBchevelle68\", \"Ana\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "Ana")
		CP.print_pass("[PASS] no errors thrown and retrieved \"Ana\"", prefix="\t")
		coreObj.check_n_set_tracker(coreObj.SUCCESS)
		coreObj.inc_pass()
	except Exception as testError:
		CP.print_fail("[FAIL] Unexpected Error thrown", prefix="\t")
		CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
		core.print_strace()
		coreObj.check_n_set_tracker(coreObj.FAILURE)
		coreObj.inc_fail()

	try:
		coreObj.inc_total()
		CP.print_info("\nTest 1.5 - Overwatch(\"HBchevelle68\", \"Anna\")", prefix="\n")
		test_OW_class_init("HBchevelle68", "Anna")
		CP.print_pass("[PASS] no errors thrown and retrieved \"Ana\"", prefix="\t")
		CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError....but returned success", prefix="\t\t")
		coreObj.check_n_set_tracker(coreObj.FAILURE)
		coreObj.inc_fail()
	except Exception as testError:
		if type(testError).__name__ is "InvalidHeroNameError":
			CP.print_pass("[PASS] threw expected InvalidHeroNameError", prefix="\t")
			coreObj.check_n_set_tracker(coreObj.SUCCESS)
			coreObj.inc_pass()
		else:
			CP.print_fail("[FAIL] Should have thrown --> InvalidHeroNameError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			core.print_strace()
			coreObj.check_n_set_tracker(coreObj.FAILURE)
			coreObj.inc_fail()