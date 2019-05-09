import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
from overwatch import overwatch

from core import core
from utils.colorprint import ColorPrint as CP

# Consts
SUCCESS = 1
FAILURE = 0

# Decorator abuse to clean up the tests
def run_test(expected_exception):
	def fn_wrapper(fn):
		def wrapper(*args, **kwargs):
			pass





# Generic Test 1 function
def test_OW_class_init(arg1):
    test = overwatch.Overwatch(arg1)
    print("Battlenet name: " , test.bnet_name)


def OW_Class_test_1(tracker):
	# Test 1.1
	try:
		CP.print_info("Test 1.1 -- Overwatch(None)", prefix="\n")
		test_OW_class_init(None)
		CP.print_fail("[FAIL] Should have thrown --> EmptyAccountStringError....but returned success", prefix="\t\t")
		tracker.inc_fail()
	except Exception as testError:
		if type(testError).__name__ is "EmptyAccountStringError":
			CP.print_pass("[PASS] threw expected EmptyAccountStringError", prefix="\t")
			tracker.inc_pass()
		else:
			CP.print_fail("[FAIL] Should have thrown --> EmptyAccountStringError", prefix="\t")
			CP.print_fail("Recveived --> %s:%s" % (type(testError).__name__, testError), prefix="\t\t")
			core.print_strace()
			tracker.inc_fail()

	"""

	 more tests are needed as it sits, there are no tests
	 showing successful execution or edge cases such as
	 an valid attempt but incorrectly spelled name
	 
	"""