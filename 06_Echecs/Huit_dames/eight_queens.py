# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=C0411, W0613

################################################################################

""" eight_queens """

################################################################################

import  argparse
import  numpy       as np
import  time

from    numba       import njit
from    time        import perf_counter

################################################################################

FGWHITE_BGGRAY  = "\033[38;5;255;48;5;8m"
FGBLACK_BGGREEN = "\033[38;5;0;48;5;82m"
FGWHITE_BGBLUE  = "\033[38;5;255;48;5;27m"
BGCYAN          = "\033[48;5;50m"
EMPTY           = "\033[0m"
PREV            = "\033[F"
UP              = "\033[A"

################################################################################

@njit(cache = True)
def eight_queens(board, delay):
    """ eight_queens function """
    dim         = board.shape[0]
    solutions   = []
    col         = 0
    row         = 0

    while col < dim:
        while row < dim:
            queen = (row, col)
            if is_well_placed(queen, solutions):
                solutions.append(queen)
                if delay != -1:
                   time.sleep(delay)
                   print_chessboard(dim, solutions)
                break
            row += 1

        row = 0

        if len(solutions) <= col:
            s = solutions.pop()

            if s[0] + 1 < dim:
                row = s[0] + 1
                col -= 1
            elif solutions:
                s = solutions.pop()
                row = s[0] + 1
                col -= 2
            else:
                break
        else:
            col += 1

    return solutions

################################################################################

@njit(cache = True)
def is_well_placed(queen, solutions):
    """ is_well_placed function """
    for s in solutions:
        if s[0] == queen[0]:
            return False
        if np.abs(s[0] - queen[0]) == np.abs(s[1] - queen[1]):
            return False

    return True

################################################################################

def print_chessboard(dim, solutions):
    """ print_chessboard function """
    board   = np.zeros((dim, dim), dtype = np.uint8)
    letters = "ABCDEFGH" * 8

    for queen in solutions:
        board[queen[0]][queen[1]] = 1

    print()

    for i in range(0, dim):
        print(f"{FGWHITE_BGBLUE} {i+1:02d} {FGWHITE_BGGRAY}", end = "")
        for j in range(0, dim):
            if board[i][j] == 0:
                print(" - ", end = "")
            else:
                print(f"{FGBLACK_BGGREEN} Q {FGWHITE_BGGRAY}", end = "")
        print("\n", end = "")

    print(f"{BGCYAN}    ", end = "")

    for i in range(0, dim):
        print(f"{FGWHITE_BGBLUE} {letters[i]} ", end = "")

    print(f"\n{EMPTY}")

    for i in range(0, dim + 3):
        print(UP, PREV)

################################################################################

def check_dimension(value):
    """ check_dimension function """
    dimension = int(value)

    if dimension < 0 or dimension > 64:
        raise argparse.ArgumentTypeError(f"DIMENSION must be between 0 and 64, got {dimension}.")

    return dimension

def check_delay(value):
    """ check_delay function """
    delay = int(value)

    if delay not in [0, 1] and delay != -1:
        raise argparse.ArgumentTypeError(f"DELAY must be 0, 1 or -1, got {delay}.")

    return delay

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("DIMENSION", help = "Values between 0 and 64.", type = check_dimension)
    parser.add_argument("DELAY",  help = "Values between 0 and 1 or -1.", type = check_delay)

    return parser.parse_args()

################################################################################

def main():
    """ main function """
    args        = check_args()

    dim         = args.DIMENSION
    delay       = args.DELAY

    t_start     = perf_counter()
    chessboard  = np.zeros((dim, dim), dtype = np.uint8)
    solutions   = eight_queens(chessboard, delay)
    t_end       = perf_counter() - t_start

    print_chessboard(dim, solutions)
    print("\n" * (dim + 2))
    print(f"Execution time : {t_end:.2f}s.")

################################################################################

if __name__ == "__main__":
    main()

################################################################################
