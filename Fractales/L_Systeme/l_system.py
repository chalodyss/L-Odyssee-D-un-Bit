# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

# pylint: disable=R0903

################################################################################

""" L-System """

################################################################################

import sys

################################################################################

class LSystem:
    """ LSystem Class """

    def __init__(self, alphabet, constants, axiom, rules):
        self.alphabet   = alphabet
        self.constants  = constants
        self.axiom      = axiom
        self.rules      = rules
        self.result     = [ self.axiom ]

################################################################################

    def compute(self, iterations):
        """ compute function """
        print(self.result)

        tmp_result  = []
        operations  = []

        for rule in self.rules.split(","):
            rule = rule.split("=")
            operations.append((rule[0], rule[1]))

        for _ in range(0, iterations):
            for token in self.result:
                for rule in operations:
                    for letter in token:
                        if letter == rule[0]:
                            tmp_result.append(rule[1])
            self.result = tmp_result[:]
            tmp_result  = []
            print(self.result)

################################################################################

def main():
    """ main function """
    alphabet    = sys.argv[1]
    constants   = sys.argv[2]
    axiom       = sys.argv[3]
    rules       = sys.argv[4]
    iterations  = int(sys.argv[5])

    l_system    = LSystem(alphabet, constants, axiom, rules)

    l_system.compute(iterations)

################################################################################

if __name__ == "__main__":
    main()

################################################################################
