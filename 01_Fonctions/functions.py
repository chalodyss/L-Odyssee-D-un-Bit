# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=C0301

################################################################################

""" functions """

################################################################################

import re

################################################################################

def hello():
    """ hello function """
    print("hello")

################################################################################

def print_nbs(n):
    """ print_nbs function """
    for i in range(0, n + 1):
        print(f"{i} ", end = "")

################################################################################

def print_alphabet():
    """ print_alphabet function """
    for c in range(97, 123):
        print(f"{chr(c)} ", end = "")

################################################################################

def count_vowels(word):
    """ count_vowels function """
    nb = 0

    for letter in word:
        if letter in "aeiouyAEIOUY":
            nb += 1

    return nb

################################################################################

def count_consonants(word):
    """ count_consonants function """
    nb = 0

    for letter in word:
        if letter.isalpha() and letter not in "aeiouy":
            nb += 1

    return nb

################################################################################

def is_palindrome(word):
    """ is_palindrome function """
    word    = word.lower()
    i       = 0
    j       = len(word) - 1

    while i < j:
        if word[i] != word[j]:
            return False
        i += 1
        j -= 1

    return True

################################################################################

def nb_abs(nb):
    """ nb_abs function """
    return -nb if nb < 0 else nb

################################################################################

def is_prime(nb):
    """ is_prime function """
    if nb < 2:
        return False
    if nb == 2:
        return True
    for i in range(3, int(nb ** 0.5) + 1, 2):
        if nb % i == 0:
            return False

    return True

################################################################################

def is_perfect(nb):
    """ is_perfect function """
    if nb <= 1:
        return False

    sum_div = 1

    for i in range(2, int(nb ** 0.5) + 1):
        if nb % i == 0:
            sum_div += i
            if i != nb // i:
                sum_div += nb // i

    return sum_div == nb

################################################################################

def binary_conv(nb):
    """ binary_conv function """
    if nb == 0:
        return "0"

    binary = []

    while nb > 0:
        binary.insert(0, str(nb % 2))
        nb = nb // 2

    return "".join(binary)

################################################################################

def base_conv(nb, base):
    """ base_conv function """
    if nb == 0:
        return "0"

    digits = "0123456789ABCDEF"
    result = []

    while nb > 0:
        result.insert(0, digits[nb % base])
        nb = nb // base

    return "".join(result)

################################################################################

def cesar_cipher(plain_text, key):
    """ cesar_cipher function """
    cipher = ""

    for c in plain_text:
        cipher += (chr((ord(c) - ord('a') + key) % 26 + ord('a')))

    return cipher

################################################################################

def bubble_sort(array):
    """ bubble_sort function """
    n = len(array)

    for i in range(0, n):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]

    return array

################################################################################

def nb_occurrences(array, limit):
    """ nb_occurrences function """
    count = [0] * limit

    for num in array:
        count[num] += 1

    for i, c in enumerate(count):
        if c > 0:
            print(f"[ {i} ] -> {count[i]}")

################################################################################

def postfix(expr):
    """ postfix function """
    stack       = []
    tokens      = expr.split(" ")
    operators   = re.compile(r'[+\-*/]')

    for token in tokens:
        if operators.match(token):
            b = stack.pop()
            a = stack.pop()

            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
        else:
            stack.append(int(token))

    return stack.pop()

################################################################################

def main():
    """ main function """
    hello()
    print_nbs(10)
    print()
    print_alphabet()
    print()
    print(f"Nombre de voyelles dans chArles                         : {count_vowels("chArles")}")
    print(f"Nombre de consonnes dans Charles                        : {count_consonants("Charles")}")
    print(f"Palindromes : Maeva - Radar                             : {is_palindrome("Maeva")} - {is_palindrome("Radar")}")
    print(f"Valeur absolue de -7                                    : {nb_abs(-7)}")
    print(f"Le nombre 101 est premier                               : {is_prime(101)}")
    print(f"Le nombre 496 est parfait                               : {is_perfect(496)}")
    print(f"Représentation binaire de 27                            : {binary_conv(27)}")
    print(f"Représentation binaire de 2500                          : {base_conv(2500, 2)}")
    print(f"Représentation octale de 2500                           : {base_conv(2500, 8)}")
    print(f"Représentation hexadécimale de 2500                     : {base_conv(2500, 16)}")
    print(f"Cipher                                                  : {cesar_cipher('abcdefghijklmnopqrstuvwxyz', 4)}")
    print(f"Tableau trié                                            : {bubble_sort([3, 6, 8, 10, 1, 2, 1])}")
    print("Occurrences [1, 2, 2, 3, 3, 3, 4, 7, 7, 7, 7, 7]         : ")
    nb_occurrences([1, 2, 2, 3, 3, 3, 4, 7, 7, 7, 7, 7], 10)
    print(f"Résultat de l'expression postfixée [3 2 * 6 + 3 - 3 /]  : {postfix("3 2 * 6 + 3 - 3 /")}")

################################################################################

if __name__ == "__main__":
    main()

################################################################################
