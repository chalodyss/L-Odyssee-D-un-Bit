# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

""" recursivity """

################################################################################

def print_numbers_recursive(n):
    """ print_numbers_recursive function """
    if n >= 0:
        print_numbers_recursive(n - 1)
        print(n, end = " ")

################################################################################

def print_numbers_iterative(n):
    """ print_numbers_iterative function """
    for i in range(0, n + 1):
        print(i, end = " ")

################################################################################

def factorial_recursive(n, acc):
    """ factorial_recursive function """
    if n < 2:
        return acc

    return factorial_recursive(n - 1, n * acc)

################################################################################

def factorial_iterative(n):
    """ factorial_iterative function """
    res = 1

    for i in range(n, 1, -1):
        res *= i

    return res

################################################################################

def fibonacci_recursive(n):
    """ fibonacci_recursive function """
    if n == 0:
        return 0
    if n == 1:
        return 1

    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)

################################################################################

def fibonacci_iterative(n):
    """ fibonacci_iterative function """
    res = 0
    n1  = 0
    n2  = 1

    if n == 0:
        res = n1
    elif n == 1:
        res = n2
    else:
        for _ in range(1, n):
            res = n1 + n2
            n1  = n2
            n2  = res

    return res

################################################################################

def hanoi_recursive(disks, start, end, tmp):
    """ hanoi_recursive function """
    if disks > 0:
        hanoi_recursive.steps += 1
        hanoi_recursive(disks - 1, start, tmp, end)
        print(f"{disks}   {start} -> {end}   {tmp}")
        hanoi_recursive(disks - 1, tmp, end, start)

    return hanoi_recursive.steps

hanoi_recursive.steps = 0

################################################################################

def hanoi_iterative(towers):
    """ hanoi_iterative function """
    stack = [ { "disks" : towers, "s" : 1, "i" : 3, "e" : 2 } ]
    steps = 0

    while stack:
        action  = stack.pop()
        disks   = action["disks"]
        start   = action["s"]
        end     = action["e"]
        tmp     = action["i"]

        if disks == 1:
            print(f"{disks}   {start} -> {end}   {tmp}")
            steps += 1
        else:
            stack.append({ "disks" : disks - 1, "s" : tmp, "e" : end, "i" : start })
            stack.append({ "disks" : 1, "s" : start, "e" : end, "i" : tmp })
            stack.append({ "disks" : disks - 1, "s" : start, "e" : tmp, "i" : end })

    return steps

################################################################################

def ackermann_recursive(m, n):
    """ ackermann_recursive function """
    if m == 0:
        return n + 1
    if m == 1:
        return n + 2
    if m == 2:
        return 2 * n + 3
    if m == 3:
        return 8 * (2**n - 1) + 5
    if n == 0:
        return ackermann_recursive(m - 1, 1)

    return ackermann_recursive(m - 1, ackermann_recursive(m, n - 1))

################################################################################

def ackermann_iterative(m, n):
    """ ackermann_iterative function """
    stack   = [ m ]
    res     = n

    while stack:
        m = stack.pop()

        if m == 0:
            res = res + 1
        elif m == 1:
            res = res + 2
        elif m == 2:
            res = 2 * res + 3
        elif m == 3:
            res = 8 * (2**res - 1) + 5
        elif res == 0:
            res = 1
            stack.append(m - 1)
        else:
            res -= 1
            stack.append(m - 1)
            stack.append(m)

    return res

################################################################################
