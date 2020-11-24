
from wordsearch import do_if_straight


def test_1():
    """Checks if good for the right arrow"""
    word = "try"
    matrix = [["t", "r", "y"], ["r", "t", "y"]]
    direction = "r"
    if do_if_straight(word, matrix, direction) == 1:
        print("Passed test 1")
    else:
        print("Test 1 failed")


def test_2():
    """Checks if good for the left arrow"""
    word = "try"
    matrix = [["t", "r", "y"], ["y", "r", "t"], ["t", "g", "l"]]
    direction = "l"
    if do_if_straight(word, matrix, direction) == 1:
        print("Passed test 2")
    else:
        print("Test 2 failed")


def test_3():
    """Checks if good for the down arrow"""
    word = "try"
    matrix = [["t", "r", "y"], ["r", "r", "t"], ["y", "g", "l"]]
    direction = "d"
    if do_if_straight(word, matrix, direction) == 1:
        print("Passed test 3")
    else:
        print("Test 3 failed")


def test_4():
    """Checks if good for the up arrow"""
    word = "try"
    matrix = [["y", "y", "y"], ["r", "r", "t"], ["t", "r", "y"]]
    direction = "u"
    if do_if_straight(word, matrix, direction) == 1:
        print("Passed test 4")
    else:
        print("Test 4 failed")


def check_do_if_straight():
    """Checks if the function do_if_straight works good."""
    test_1()
    test_2()
    test_3()
    test_4()


if __name__ == "__main__":
    check_reorder_l()
