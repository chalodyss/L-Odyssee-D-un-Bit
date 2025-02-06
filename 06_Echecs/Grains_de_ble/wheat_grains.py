# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

""" wheat_grains """

################################################################################

import argparse

################################################################################

def wheat_grains(nb_cases, verbose = 0):
    """ wheat_grains function """
    total = 0

    if verbose == 1:
        for i in range(0, nb_cases):
            total   += (2 ** i)
            mass    = total * 0.00000004
            print(f"{i:2} Total: {total:<30_} - Mass: {round(mass, 1):_} tons.")
    else:
        total   =  2 ** nb_cases - 1
        mass    = total * 0.00000004

    return total, mass

################################################################################

def check_nbcases(value):
    """ check_nbcases function """
    nb_cases = int(value)

    if nb_cases < 0 or nb_cases > 64:
        raise argparse.ArgumentTypeError(f"NB_CASES must be between 0 and 64, got {nb_cases}.")

    return nb_cases

def check_verbose(value):
    """ check_verbose function """
    verbose = int(value)

    if verbose not in [0, 1]:
        raise argparse.ArgumentTypeError(f"VERBOSE must be 0 or 1, got {verbose}.")

    return verbose

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("NB_CASES", help = "Values between 0 and 64.", type = check_nbcases)
    parser.add_argument("VERBOSE",  help = "Values between in {0, 1}.", type = check_verbose)

    return parser.parse_args()

################################################################################

def main():
    """ main function """
    args        = check_args()

    nb_cases    = args.NB_CASES
    verbose     = args.VERBOSE
    result      = wheat_grains(nb_cases, verbose)

    print("-" * 40)
    print(f"Number of grains : {result[0]:_}.")
    print(f"Mass of wheat    : {round(result[1], 1):_} tons.")
    print("-" * 40)

################################################################################

if __name__ == "__main__":
    main()

################################################################################
