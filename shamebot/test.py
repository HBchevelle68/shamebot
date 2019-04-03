from overwatch import temp
import art

def test_OW_class_init(arg1, arg2):
    test = temp.Overwatch(arg1, arg2)
    print("Battlenet name: " , test.bnet_name)
    print("Hero:            %s " % test.hero)
    print("Hero Value:      %d " % test.hero_val)

art.printart()

print("\n**** Begin testing ****")

print("\nTest 1 -- Overwatch()")
test_OW_class_init(None, None)

print("\nTest 2 - Overwatch(\"HBchevelle68\")")
test_OW_class_init("HBchevelle68", None)

print("\nTest 3 -- Overwatch(\"HBchevelle68\", \"Ana\")")
test_OW_class_init("HBchevelle68", "Ana")

print("\nTest 4 -- Overwatch(\"HBchevelle68\", \"Anna\")")
test_OW_class_init("HBchevelle68", "Anna")
