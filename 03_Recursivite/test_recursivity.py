# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=W0401

################################################################################

""" test_recursivity """

################################################################################

import  sys

from    recursivity import *

################################################################################

def test_print_numbers_recursive(capsys):
    """ test_print_numbers_recursive function """
    print_numbers_recursive(0)
    captured = capsys.readouterr()
    assert captured.out == "0 "
    print_numbers_recursive(2)
    captured = capsys.readouterr()
    assert captured.out == "0 1 2 "
    print_numbers_recursive(8)
    captured = capsys.readouterr()
    assert captured.out == "0 1 2 3 4 5 6 7 8 "

################################################################################

def test_print_numbers_iterative(capsys):
    """ test_print_numbers_iterative function """
    print_numbers_iterative(0)
    captured = capsys.readouterr()
    assert captured.out == "0 "
    print_numbers_iterative(2)
    captured = capsys.readouterr()
    assert captured.out == "0 1 2 "
    print_numbers_iterative(8)
    captured = capsys.readouterr()
    assert captured.out == "0 1 2 3 4 5 6 7 8 "

################################################################################

def test_factorial_recursive():
    """ test_factorial_recursive function """
    assert factorial_recursive(0, 1)  == 1
    assert factorial_recursive(1, 1)  == 1
    assert factorial_recursive(2, 1)  == 2
    assert factorial_recursive(4, 1)  == 24
    assert factorial_recursive(8, 1)  == 40320

################################################################################

def test_factorial_iterative():
    """ test_factorial_iterative function """
    assert factorial_iterative(0)  == 1
    assert factorial_iterative(1)  == 1
    assert factorial_iterative(2)  == 2
    assert factorial_iterative(4)  == 24
    assert factorial_iterative(8)  == 40320

################################################################################

def test_fibonacci_recursive():
    """ test_fibonacci_recursive function """
    assert fibonacci_recursive(0)  == 0
    assert fibonacci_recursive(1)  == 1
    assert fibonacci_recursive(2)  == 1
    assert fibonacci_recursive(3)  == 2
    assert fibonacci_recursive(4)  == 3
    assert fibonacci_recursive(5)  == 5
    assert fibonacci_recursive(8)  == 21
    assert fibonacci_recursive(10) == 55

################################################################################

def test_fibonacci_iterative():
    """ test_fibonacci_iterative function """
    assert fibonacci_iterative(0)  == 0
    assert fibonacci_iterative(1)  == 1
    assert fibonacci_iterative(2)  == 1
    assert fibonacci_iterative(3)  == 2
    assert fibonacci_iterative(4)  == 3
    assert fibonacci_iterative(5)  == 5
    assert fibonacci_iterative(8)  == 21
    assert fibonacci_iterative(10) == 55

################################################################################

def test_hanoi_recursive():
    """ test_hanoi_recursive function """
    assert hanoi_recursive(0, 1, 3, 2)  == 0
    hanoi_recursive.steps = 0
    assert hanoi_recursive(1, 1, 3, 2)  == 1
    hanoi_recursive.steps = 0
    assert hanoi_recursive(2, 1, 3, 2)  == 3
    hanoi_recursive.steps = 0
    assert hanoi_recursive(3, 1, 3, 2)  == 7
    hanoi_recursive.steps = 0
    assert hanoi_recursive(8, 1, 3, 2)  == 255
    hanoi_recursive.steps = 0
    assert hanoi_recursive(16, 1, 3, 2) == 65535

################################################################################

def test_hanoi_iterative():
    """ test_hanoi_iterative function """
    assert hanoi_iterative(1)  == 1
    assert hanoi_iterative(2)  == 3
    assert hanoi_iterative(3)  == 7
    assert hanoi_iterative(8)  == 255
    assert hanoi_iterative(16) == 65535

################################################################################

def test_ackermann_recursive():
    """ test_ackermann_recursive function """
    sys.setrecursionlimit(10000)
    sys.set_int_max_str_digits(20000)

    assert ackermann_recursive(0, 0)              == 1
    assert ackermann_recursive(0, 1)              == 2
    assert ackermann_recursive(0, 6)              == 7
    assert ackermann_recursive(1, 0)              == 2
    assert ackermann_recursive(1, 1)              == 3
    assert ackermann_recursive(1, 6)              == 8
    assert ackermann_recursive(2, 0)              == 3
    assert ackermann_recursive(2, 2)              == 7
    assert ackermann_recursive(2, 4)              == 11
    assert ackermann_recursive(3, 0)              == 5
    assert ackermann_recursive(3, 2)              == 29
    assert ackermann_recursive(3, 4)              == 125
    assert ackermann_recursive(4, 0)              == 13
    assert ackermann_recursive(4, 1)              == 65533
    assert len(str(ackermann_recursive(4, 2)))    == 19729

################################################################################

def test_ackermann_iterative():
    """ test_ackermann_iterative function """
    sys.setrecursionlimit(10000)
    sys.set_int_max_str_digits(20000)

    assert ackermann_iterative(0, 0)              == 1
    assert ackermann_iterative(0, 1)              == 2
    assert ackermann_iterative(0, 6)              == 7
    assert ackermann_iterative(1, 0)              == 2
    assert ackermann_iterative(1, 1)              == 3
    assert ackermann_iterative(1, 6)              == 8
    assert ackermann_iterative(2, 0)              == 3
    assert ackermann_iterative(2, 2)              == 7
    assert ackermann_iterative(2, 4)              == 11
    assert ackermann_iterative(3, 0)              == 5
    assert ackermann_iterative(3, 2)              == 29
    assert ackermann_iterative(3, 4)              == 125
    assert ackermann_iterative(4, 0)              == 13
    assert ackermann_iterative(4, 1)              == 65533
    assert len(str(ackermann_iterative(4, 2)))    == 19729

################################################################################
