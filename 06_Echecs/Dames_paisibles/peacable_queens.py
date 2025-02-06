# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=C0301, C0321, C0411, R0902, R0911, R0913, R0914, R0917, R1702, W0621

################################################################################

""" peacable_queens """

################################################################################

import  argparse
import  numpy               as np

from    functools           import partial
from    multiprocessing     import Pool
from    numba               import njit

################################################################################

BLUE    = "\033[1;34m"
GREEN   = "\033[1;92m"
EMPTY   = "\033[0m"
PREV    = "\033[F"
UP      = "\033[A"

################################################################################

def display(chessboard, dim):
    """ display function """
    print()
    print(" ", end = "")
    print("-" * (dim * 3 + 2))

    for i in range(0, dim):
        print(" |", end = "")

        for j in range(0, dim):
            if chessboard[i][j] == 0:
                print(" . ", end = "")
            elif chessboard[i][j] == 1:
                print(f"{BLUE} W {EMPTY}", end = "")
            else:
                print(f"{GREEN} B {EMPTY}", end = "")

        print("|")

    print(" ", end = "")
    print("-" * (dim * 3 + 2))

################################################################################

def terminate(result, dim, pool):
    """ terminate function """
    print(f"\nBest solution [{result[1]}] found at generation {result[2]}\n")
    display(result[0], dim)

    pool.terminate()

################################################################################

@njit(cache = True)
def init_random(dim, nb_organisms, nb_queens, population):
    """ init_random function """
    for i in range(0, nb_organisms):
        data                = np.zeros(dim * dim, dtype = np.uint8)
        data[:nb_queens]    = 1
        data[-nb_queens:]   = 2

        np.random.shuffle(data)

        population[i]       = data.reshape((dim, dim))

    return population

@njit(cache = True)
def init_middle(dim, nb_organisms, nb_queens, population):
    """ init_middle function """
    for i in range(0, nb_organisms):
        data                = np.zeros(dim * dim, dtype = np.uint8)

        data[:nb_queens]    = 1
        data[-nb_queens:]   = 2

        population[i]       = data.reshape((dim, dim))

    return population

@njit(cache = True)
def partition(dim):
    """ partition function """
    base        = dim // 4
    remainder   = dim % 4
    sizes       = np.zeros(4, dtype = np.uint8)

    for i in range(0, 4):
        sizes[i] = base + (1 if i < remainder else 0)

    boundaries  = np.zeros(5, dtype = np.uint8)

    for i in range(1, 5):
        boundaries[i] = boundaries[i - 1] + sizes[i - 1]

    return boundaries

@njit(cache = True)
def init_quarter(dim, nb_organisms, nb_queens, population, boundaries):
    """ init_quarter function """
    white_first_quarter     = nb_queens // 2
    white_third_quarter     = nb_queens - white_first_quarter

    black_second_quarter    = nb_queens // 2
    black_last_quarter      = nb_queens - black_second_quarter

    for i in range(0, nb_organisms):
        data    = np.zeros(dim * dim, dtype = np.uint8)
        board   = data.reshape(dim, dim)

        width_1 = boundaries[1] - boundaries[0]

        for j in range(white_first_quarter):
            row = j // width_1
            col = boundaries[0] + (j % width_1)

            if row < dim:
                board[row, col] = 1

        width_3 = boundaries[3] - boundaries[2]

        for j in range(white_third_quarter):
            row = j // width_3
            col = boundaries[2] + (j % width_3)

            if row < dim:
                board[row, col] = 1

        width_2 = boundaries[2] - boundaries[1]

        for j in range(black_second_quarter):
            row = dim - 1 - (j // width_2)
            col = boundaries[1] + (j % width_2)

            if row >= 0:
                board[row, col] = 2

        width_4 = boundaries[4] - boundaries[3]

        for j in range(black_last_quarter):
            row = dim - 1 - (j // width_4)
            col = boundaries[3] + (j % width_4)

            if row >= 0:
                board[row, col] = 2

        population[i] = board

    return population

################################################################################

@njit(cache = True)
def reset_quarter(dim, nb_queens, boundaries):
    """ init_quarter function """
    white_first_quarter     = nb_queens // 2
    white_third_quarter     = nb_queens - white_first_quarter

    black_second_quarter    = nb_queens // 2
    black_last_quarter      = nb_queens - black_second_quarter

    data                    = np.zeros(dim * dim, dtype = np.uint8)
    board                   = data.reshape(dim, dim)

    width_1 = boundaries[1] - boundaries[0]

    for j in range(white_first_quarter):
        row = j // width_1
        col = boundaries[0] + (j % width_1)

        if row < dim:
            board[row, col] = 1

    width_3 = boundaries[3] - boundaries[2]

    for j in range(white_third_quarter):
        row = j // width_3
        col = boundaries[2] + (j % width_3)

        if row < dim:
            board[row, col] = 1

    width_2 = boundaries[2] - boundaries[1]

    for j in range(black_second_quarter):
        row = dim - 1 - (j // width_2)
        col = boundaries[1] + (j % width_2)

        if row >= 0:
            board[row, col] = 2

    width_4 = boundaries[4] - boundaries[3]

    for j in range(black_last_quarter):
        row = dim - 1 - (j // width_4)
        col = boundaries[3] + (j % width_4)

        if row >= 0:
            board[row, col] = 2

    return board

################################################################################

@njit(fastmath = True, cache = True)
def eval_fitnesses(dim, nb_organisms, nb_queens, population,
                   fitnesses, b_fitnesses, w_fitnesses):
    """ eval_fitnesses function """
    for i in range(nb_organisms):
        organism    = population[i]

        b_n         = nb_queens
        w_n         = nb_queens

        wi, wj      = np.where(organism == 1)
        bi, bj      = np.where(organism == 2)

        rows_w      = np.zeros(dim, dtype = np.uint8)
        cols_w      = np.zeros(dim, dtype = np.uint8)
        diag1_w     = np.zeros(2 * dim - 1, dtype = np.uint8)
        diag2_w     = np.zeros(2 * dim - 1, dtype = np.uint8)

        for j in range(nb_queens):
            rows_w[wi[j]]                       = 1
            cols_w[wj[j]]                       = 1
            diag1_w[wi[j] + wj[j]]              = 1
            diag2_w[wi[j] - wj[j] + dim - 1]    = 1

        for j in range(nb_queens):
            row     = bi[j]
            col     = bj[j]
            diag1   = row + col
            diag2   = row - col + dim - 1

            if rows_w[row] or cols_w[col] or diag1_w[diag1] or diag2_w[diag2]:
                b_n -= 1

        rows_b      = np.zeros(dim, dtype = np.uint8)
        cols_b      = np.zeros(dim, dtype = np.uint8)
        diag1_b     = np.zeros(2 * dim - 1, dtype = np.uint8)
        diag2_b     = np.zeros(2 * dim - 1, dtype = np.uint8)

        for j in range(nb_queens):
            rows_b[bi[j]]                       = 1
            cols_b[bj[j]]                       = 1
            diag1_b[bi[j] + bj[j]]              = 1
            diag2_b[bi[j] - bj[j] + dim - 1]    = 1

        for j in range(nb_queens):
            row     = wi[j]
            col     = wj[j]
            diag1   = row + col
            diag2   = row - col + dim - 1

            if rows_b[row] or cols_b[col] or diag1_b[diag1] or diag2_b[diag2]:
                w_n -= 1

        b_fitnesses[i]  = b_n / nb_queens
        w_fitnesses[i]  = w_n / nb_queens
        fitnesses[i]    = (b_n + w_n) / (nb_queens * 2)

@njit(fastmath = True, cache = True)
def eval_fitness(dim, nb_queens, organism):
    """ eval_fitness function """
    b_n     = nb_queens
    w_n     = nb_queens

    wi, wj  = np.where(organism == 1)
    bi, bj  = np.where(organism == 2)

    rows_w  = np.zeros(dim, dtype = np.uint8)
    cols_w  = np.zeros(dim, dtype = np.uint8)
    diag1_w = np.zeros(2 * dim -1, dtype = np.uint8)
    diag2_w = np.zeros(2 * dim -1, dtype = np.uint8)

    for i in range(nb_queens):
        rows_w[wi[i]]                   = 1
        cols_w[wj[i]]                   = 1
        diag1_w[wi[i] + wj[i]]          = 1
        diag2_w[wi[i] - wj[i] + dim -1] = 1

    for i in range(nb_queens):
        row     = bi[i]
        col     = bj[i]
        diag1   = row + col
        diag2   = row - col + dim -1

        if rows_w[row] or cols_w[col] or diag1_w[diag1] or diag2_w[diag2]:
            b_n -= 1

    rows_b  = np.zeros(dim, dtype = np.uint8)
    cols_b  = np.zeros(dim, dtype = np.uint8)
    diag1_b = np.zeros(2 * dim - 1, dtype = np.uint8)
    diag2_b = np.zeros(2 * dim - 1, dtype = np.uint8)

    for i in range(nb_queens):
        rows_b[bi[i]]                   = 1
        cols_b[bj[i]]                   = 1
        diag1_b[bi[i] + bj[i]]          = 1
        diag2_b[bi[i] - bj[i] + dim - 1] = 1

    for i in range(nb_queens):
        row     = wi[i]
        col     = wj[i]
        diag1   = row + col
        diag2   = row - col + dim - 1

        if rows_b[row] or cols_b[col] or diag1_b[diag1] or diag2_b[diag2]:
            w_n -= 1

    return (b_n + w_n) / (nb_queens * 2)

################################################################################

@njit(fastmath = True, cache = True)
def normalize_probabilities(nb_organisms, probabilities, fitnesses):
    """ normalize function """
    n = 0

    for f in fitnesses:
        n += f

    for i in range(0, nb_organisms):
        probabilities[i] = fitnesses[i] / n if n != 0 else 0

################################################################################

@njit(fastmath = True, cache = True)
def selection(dim, nb_organisms, population, probabilities):
    """ selection function """
    size        = 0
    frequencies = np.zeros((nb_organisms), dtype = np.uint16)

    for i in range(0, nb_organisms):
        n               = 1
        n               += int(probabilities[i] * nb_organisms)
        n               -= 1 if n > 1 else 0
        frequencies[i]  = n
        size            += n

    incubator   = np.zeros(shape = (size, dim, dim), dtype = np.uint16)
    references  = np.zeros(shape = (size), dtype = np.uint16)
    indice      = 0

    for i in range(0, nb_organisms):
        for j in range(0, frequencies[i]):
            incubator[indice + j]   = population[i]
            references[indice + j]  = i

        indice += frequencies[i]

    return incubator, references

################################################################################

@njit(cache = True)
def is_well_placed(chessboard, queen, color):
    """ is_well_placed function """
    q_row   = queen[0]
    q_col   = queen[1]
    enemy   = 1 if color == 2 else 1
    size    = chessboard.shape[0]

    for i in range(size):
        if i != q_col and chessboard[q_row, i] == enemy:
            return False
        if i != q_row and chessboard[i, q_col] == enemy:
            return False

    for i in range(1, size):
        if q_row - i >= 0 and q_col - i >= 0:
            if chessboard[q_row - i, q_col - i] == enemy:
                return False

        if q_row - i >= 0 and q_col + i < size:
            if chessboard[q_row - i, q_col + i] == enemy:
                return False

        if q_row + i < size and q_col - i >= 0:
            if chessboard[q_row + i, q_col - i] == enemy:
                return False

        if q_row + i < size and q_col + i < size:
            if chessboard[q_row + i, q_col + i] == enemy:
                return False

    return True

################################################################################

@njit(cache = True)
def crossover(x, y, b_fitness, w_fitness):
    """ crossover function """
    if b_fitness <= w_fitness:
        dad_black_queens = np.argwhere(x == 2)
        mum_black_queens = np.argwhere(y == 2)

        for i in range(0, dad_black_queens.shape[0]):
            d_queen = dad_black_queens[i]

            if is_well_placed(x, d_queen, 2) is False:
                for j in range(0, mum_black_queens.shape[0]):
                    m_queen = mum_black_queens[j]
                    if (is_well_placed(x, m_queen, 2) is True
                        and x[m_queen[0], m_queen[1]] == 0
                        and mum_black_queens[j][0] != 0
                        and mum_black_queens[j][1] != 0):
                        x[d_queen[0], d_queen[1]]   = 0
                        x[m_queen[0], m_queen[1]]   = 2
                        mum_black_queens[j][0]      = 0
                        mum_black_queens[j][1]      = 0
                        break

    elif w_fitness <= b_fitness:
        dad_white_queens = np.argwhere(x == 1)
        mum_white_queens = np.argwhere(y == 1)

        for i in range(0, dad_white_queens.shape[0]):
            d_queen = dad_white_queens[i]

            if is_well_placed(x, d_queen, 1) is False:
                for j in range(0, mum_white_queens.shape[0]):
                    m_queen = mum_white_queens[j]
                    if (is_well_placed(x, m_queen, 1) is True
                        and x[m_queen[0], m_queen[1]] == 0
                        and mum_white_queens[j][0] != 0
                        and mum_white_queens[j][1] != 0):
                        x[d_queen[0], d_queen[1]]   = 0
                        x[m_queen[0], m_queen[1]]   = 1
                        mum_white_queens[j][0]      = 0
                        mum_white_queens[j][1]      = 0
                        break

    return x

################################################################################

@njit(fastmath = True, cache = True)
def reproduction(dim, nb_organisms, nb_queens, population, incubator,
                 references, fitnesses, b_fitnesses, w_fitnesses):
    """ reproduction function """
    m       = 0
    n       = incubator.shape[0]
    i       = 0
    mean    = np.mean(fitnesses)
    bests   = np.argwhere(fitnesses == np.amax(fitnesses))
    flip    = 0

    for i in range(0, nb_organisms):
        x = incubator[np.random.randint(m, n)]
        y = incubator[np.random.randint(m, n)]

        if fitnesses[references[m]] > fitnesses[references[n]]:
            bf      = b_fitnesses[references[m]]
            wf      = w_fitnesses[references[m]]
            child   = crossover(x.copy(), y, bf, wf)
        else:
            bf      = b_fitnesses[references[n]]
            wf      = w_fitnesses[references[n]]
            child   = crossover(y.copy(), x, bf, wf)

        if eval_fitness(dim, nb_queens, child) > mean:
            population[i] = child
        else:
            if flip == 0:
                population[i] = population[bests[i % bests.shape[0]]]
            flip = flip ^ 1

        i += 1

################################################################################

@njit(cache = True)
def correct_random(nb_organisms, nb_queens, population,
                   b_fitnesses, w_fitnesses, fitnesses,
                   max_fitness):
    """ correct_random function """
    dim = population[0].shape[0]

    for i in range(0, nb_organisms):
        if fitnesses[i] == max_fitness:
            color   = 1 if b_fitnesses[i] > w_fitnesses[i] else 2
            queens  = np.argwhere(population[i] == color)
            cpt     = 0

            for j in range(0, nb_queens):
                if is_well_placed(population[i], queens[j], color) is False:
                    squares = np.argwhere(population[i] == 0)

                    for k in range(0, squares.shape[0]):
                        if is_well_placed(population[i], squares[k], color) is True:
                            population[i, queens[j, 0], queens[j, 1]]   = 0
                            population[i, squares[k, 0], squares[k, 1]] = color
                            cpt += 1
                            break

                if cpt == 0:
                    data                = np.zeros(dim * dim, dtype = np.uint8)
                    data[:nb_queens]    = 1
                    data[-nb_queens:]   = 2

                    np.random.shuffle(data)

                    population[i]       = data.reshape((dim, dim))
                    break

@njit(cache = True)
def correct_middle(nb_organisms, nb_queens, population,
                   b_fitnesses, w_fitnesses, fitnesses,
                   max_fitness):
    """ correct_random function """
    dim = population[0].shape[0]

    for i in range(0, nb_organisms):
        if fitnesses[i] == max_fitness:
            color   = 1 if b_fitnesses[i] > w_fitnesses[i] else 2
            queens  = np.argwhere(population[i] == color)
            cpt     = 0

            for j in range(0, nb_queens):
                if is_well_placed(population[i], queens[j], color) is False:
                    squares = np.argwhere(population[i] == 0)

                    for k in range(0, squares.shape[0]):
                        if is_well_placed(population[i], squares[k], color) is True:
                            population[i, queens[j, 0], queens[j, 1]]   = 0
                            population[i, squares[k, 0], squares[k, 1]] = color
                            cpt += 1
                            break

                if cpt == 0:
                    data                = np.zeros(dim * dim, dtype = np.uint8)
                    data[:nb_queens]    = 1
                    data[-nb_queens:]   = 2
                    population[i]       = data.reshape((dim, dim))
                    break

@njit(fastmath = True, cache = True)
def shift_white_black_queens(dim, board, prob):
    """ shift_white_black_queens function """
    half    = dim // 2
    shift   = np.random.randint(0, 2)

    if shift == 0:
        for c in range(dim):
            move_down   = np.random.rand() < prob
            white_rows  = np.where(board[:half, c] == 1)[0]

            if move_down:
                for idx in range(white_rows.size - 1, -1, -1):
                    r   = white_rows[idx]
                    nr  = r + 1

                    if nr < half and board[nr, c] == 0:
                        board[r, c]     = 0
                        board[nr, c]    = 1
            else:
                for idx in range(white_rows.size):
                    r   = white_rows[idx]
                    nr  = r - 1

                    if nr >= 0 and board[nr, c] == 0:
                        board[r, c]     = 0
                        board[nr, c]    = 1
    else:
        for c in range(dim):
            move_down   = np.random.rand() < prob
            black_rows  = np.where(board[half:dim, c] == 2)[0] + half

            if move_down:
                for idx in range(black_rows.size - 1, -1, -1):
                    r = black_rows[idx]
                    nr = r + 1

                    if nr < dim and board[nr, c] == 0:
                        board[r, c]     = 0
                        board[nr, c]    = 2
            else:
                for idx in range(black_rows.size):
                    r   = black_rows[idx]
                    nr  = r - 1

                    if nr >= half and board[nr, c] == 0:
                        board[r, c]     = 0
                        board[nr, c]    = 2

    return board

@njit(fastmath = True, cache = True)
def correct_quarter(nb_organisms, nb_queens, population, b_fitnesses,
                    w_fitnesses, fitnesses, max_fitness, boundaries):
    """ correct_quarter function """
    for i in range(0, nb_organisms):
        if fitnesses[i] == max_fitness:
            color   = 1 if b_fitnesses[i] > w_fitnesses[i] else 2
            queens  = np.argwhere(population[i] == color)
            cpt     = 0

            for j in range(0, nb_queens):
                if is_well_placed(population[i], queens[j], color) is False:
                    squares = np.argwhere(population[i] == 0)

                    for k in range(0, squares.shape[0]):
                        if is_well_placed(population[i], squares[k], color) is True:
                            population[i, queens[j, 0], queens[j, 1]]   = 0
                            population[i, squares[k, 0], squares[k, 1]] = color
                            cpt += 1
                            break

                    if cpt == 0:
                        dim             = population[i].shape[0]
                        limit           = np.random.randint(1, 3)
                        population[i]   = mutation_quarter_organism(dim, population[i], boundaries, limit)
                        break

                    break

################################################################################

@njit(fastmath = True, cache = True)
def mutation_random(nb_queens, population, limit):
    """  mutation_random function """
    for i in range(0, population.shape[0]):
        for _ in range(0, limit):
            color   = np.random.randint(1, 3)
            queens  = np.argwhere(population[i] == color)

            queen   = queens[np.random.randint(0, nb_queens)]
            cases   = np.argwhere(population[i] == 0)

            case    = cases[np.random.randint(0, cases.shape[0])]

            population[i, queen[0], queen[1]] = 0
            population[i, case[0], case[1]]   = color

@njit(fastmath = True, cache = True)
def mutation_middle(dim, nb_organisms, nb_queens, population):
    """ mutation_middle function """
    dim_half = dim // 2

    for i in range(0, nb_organisms):
        color = np.random.randint(1, 3)

        if color == 1:
            cases = np.argwhere(population[i][0:dim_half] == 0)
        else:
            cases           = np.argwhere(population[i][dim_half:dim] == 0)
            cases[:, 0:1]   += (dim_half)

        m       = np.random.randint(0, cases.shape[0])

        n       = np.random.randint(0, nb_queens)
        queen   = np.argwhere(population[i] == color)[n]

        population[i, queen[0], queen[1]]         = 0
        population[i, cases[m, 0], cases[m, 1]]   = color

@njit(fastmath = True, cache = True)
def mutation_quarter(dim, nb_organisms, population, boundaries, limit):
    """ mutation_quarter function """
    white_quarters = (0, 2)
    black_quarters = (1, 3)

    for org in range(nb_organisms):
        for _ in range(limit):
            chosen_quarter  = np.random.randint(0, 4)
            color           = 1 if chosen_quarter in white_quarters else 2

            start_col       = boundaries[chosen_quarter]
            end_col         = boundaries[chosen_quarter + 1]

            if color == 1:
                row_min, row_max = 0, dim // 2
            else:
                row_min, row_max = dim // 2, dim

            quarter_queens = []

            for r in range(row_min, row_max):
                for c in range(start_col, end_col):
                    if population[org, r, c] == color:
                        quarter_queens.append((r, c))

            if len(quarter_queens) == 0:
                continue

            idx_queen       = np.random.randint(0, len(quarter_queens))
            row_q, col_q    = quarter_queens[idx_queen]

            valid_quarters  = white_quarters if color == 1 else black_quarters

            col_positions   = []

            for q in valid_quarters:
                for cc in range(boundaries[q], boundaries[q+1]):
                    col_positions.append(cc)

            empty_spots = []

            for rr in range(row_min, row_max):
                for cc in col_positions:
                    if population[org, rr, cc] == 0:
                        empty_spots.append((rr, cc))

            if len(empty_spots) == 0:
                continue

            spot_idx                        = np.random.randint(0, len(empty_spots))
            r_spot, c_spot                  = empty_spots[spot_idx]

            population[org, row_q, col_q]   = 0
            population[org, r_spot, c_spot] = color

    return population

@njit(fastmath = True, cache = True)
def mutation_quarter_organism(dim, organism, boundaries, limit):
    """ mutation_quarter_organism function """
    white_quarters = (0, 2)
    black_quarters = (1, 3)

    for _ in range(0, limit):
        chosen_quarter  = np.random.randint(0, 4)
        color           = 1 if chosen_quarter in white_quarters else 2

        start_col       = boundaries[chosen_quarter]
        end_col         = boundaries[chosen_quarter + 1]

        if color == 1:
            row_min, row_max = 0, dim // 2
        else:
            row_min, row_max = dim // 2, dim

        quarter_queens      = []

        for r in range(row_min, row_max):
            for c in range(start_col, end_col):
                if organism[r, c] == color:
                    quarter_queens.append((r, c))

            if len(quarter_queens) == 0:
                continue

            idx_queen       = np.random.randint(0, len(quarter_queens))
            row_q, col_q    = quarter_queens[idx_queen]

            valid_quarters  = white_quarters if color == 1 else black_quarters

            col_positions   = []

            for q in valid_quarters:
                for cc in range(boundaries[q], boundaries[q+1]):
                    col_positions.append(cc)

            empty_spots     = []

            for rr in range(row_min, row_max):
                for cc in col_positions:
                    if organism[rr, cc] == 0:
                        empty_spots.append((rr, cc))

            if len(empty_spots) == 0:
                continue

            spot_idx                    = np.random.randint(0, len(empty_spots))
            r_spot, c_spot              = empty_spots[spot_idx]

            organism[row_q, col_q]      = 0
            organism[r_spot, c_spot]    = color

    return organism

################################################################################

@njit(cache = True)
def search_queens(num, dim, nb_organisms, nb_queens,
                  mutation, nb_generations, initialization, strategy):
    """ search_queens function """
    population      = np.zeros(shape = (nb_organisms, dim, dim))
    fitnesses       = np.zeros(shape = (nb_organisms), dtype = np.float32)
    b_fitnesses     = np.zeros(shape = (nb_organisms), dtype = np.float32)
    w_fitnesses     = np.zeros(shape = (nb_organisms), dtype = np.float32)
    probabilities   = np.zeros(shape = (nb_organisms), dtype = np.float32)
    boundaries      = partition(dim)
    max_fitness     = 0
    generation      = 0
    cpt             = 0
    limit           = 1
    epsilon         = 1e-2

    if initialization == 0:
        init_random(dim, nb_organisms, nb_queens, population)
    elif initialization == 1:
        init_middle(dim, nb_organisms, nb_queens, population)
    elif initialization == 2:
        init_quarter(dim, nb_organisms, nb_queens, population, boundaries)

    while cpt <= nb_generations:
        val = np.max(fitnesses)

        if val > max_fitness:
            print("Thread ", num, " : ", np.round(max_fitness, 2), "\t- Génération : ", cpt)
            max_fitness = val
            generation  = 0

        normalize_probabilities(nb_organisms, probabilities, fitnesses)
        incubator, references = selection(dim, nb_organisms, population, probabilities)

        reproduction(dim, nb_organisms, nb_queens, population, incubator,
                     references, fitnesses, b_fitnesses, w_fitnesses)

        cpt += 1

        eval_fitnesses(dim, nb_organisms, nb_queens, population,
                       fitnesses, b_fitnesses, w_fitnesses)

        if np.any(fitnesses >= 1.0 - epsilon):
            return population[np.argmax(fitnesses)], np.max(fitnesses), cpt

        if strategy == 0:
            mutation_random(nb_queens, population, limit)
        elif strategy == 1:
            mutation_middle(dim, nb_organisms, nb_queens, population)
        elif strategy == 2:
            mutation_quarter(dim, nb_organisms, population, boundaries, limit)

        if generation > mutation:
            generation = 0

            if strategy == 0:
                correct_random(nb_organisms, nb_queens, population,
                               b_fitnesses, w_fitnesses, fitnesses, max_fitness)
            elif strategy == 1:
                correct_middle(nb_organisms, nb_queens, population,
                               b_fitnesses, w_fitnesses, fitnesses, max_fitness)
            elif strategy == 2:
                correct_quarter(nb_organisms, nb_queens, population, b_fitnesses,
                                w_fitnesses, fitnesses, max_fitness, boundaries)

            flip = np.random.randint(0, 10)

            if flip == 0:
                rate        = np.random.uniform(0, 0.1)
                nb_to_reset = int(nb_organisms * rate)

                if strategy == 0:
                    init_random(dim, nb_to_reset, nb_queens, population)
                elif strategy == 1:
                    init_middle(dim, nb_to_reset, nb_queens, population)
                elif strategy == 2:
                    init_quarter(dim, nb_to_reset, nb_queens, population, boundaries)

                    for i in range(0, nb_to_reset):
                        shift_white_black_queens(dim, population[i], 1)

        generation += 1

    return (population[np.argmax(fitnesses)], np.max(fitnesses), cpt)

################################################################################

def check_dimensions(value):
    """ check_dimensions function """
    dimensions = int(value)

    if dimensions < 0 or dimensions > 64:
        raise argparse.ArgumentTypeError(f"DIMENSIONS must be between 0 and 64, got {dimensions}.")

    return dimensions

def check_organisms(value):
    """ check_organisms function """
    organisms = int(value)

    if organisms < 0 or organisms > 10000:
        raise argparse.ArgumentTypeError(f"ORGANISMS must be between 0 and 10000, got {organisms}.")

    return organisms

def check_queens(value):
    """ check_queens function """
    queens = int(value)

    if queens < 0 or queens > 1000:
        raise argparse.ArgumentTypeError(f"QUEENS must between 0 and 1000, got {queens}.")

    return queens

def check_cpus(value):
    """ check_cpus function """
    cpus = int(value)

    if cpus < 0 or cpus > 10:
        raise argparse.ArgumentTypeError(f"CPUS must between 0 and 10, got {cpus}.")

    return cpus

def check_mutation(value):
    """ check_mutation function """
    mutation = int(value)

    if mutation < 0 or mutation > 1000:
        raise argparse.ArgumentTypeError(f"MUTATION must between 0 and 1000, got {mutation}.")

    return mutation

def check_generations(value):
    """ check_generations function """
    generations = int(value)

    if generations < 1 or generations > 100000:
        raise argparse.ArgumentTypeError(f"GENERATIONS must between 1 and 100000, got {generations}.")

    return generations

def check_initialization(value):
    """ check_initialization function """
    initialization = int(value)

    if initialization not in [ 0, 1, 2 ]:
        raise argparse.ArgumentTypeError(f"INITIALIZATION must be 0, 1, 2, got {initialization}.")

    return initialization

def check_strategy(value):
    """ check_strategy function """
    strategy = int(value)

    if strategy not in [ 0, 1, 2 ]:
        raise argparse.ArgumentTypeError(f"STRATEGY must be between 0 and 2, got {strategy}.")

    return strategy

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("DIMENSIONS", help = "Values between 0 and 64.", type = check_dimensions)
    parser.add_argument("ORGANISMS",  help = "Values between 0 and 10000.", type = check_organisms)
    parser.add_argument("QUEENS",  help = "Values between 0 and 1000", type = check_queens)
    parser.add_argument("CPUS",  help = "Values between 0 and 10", type = check_cpus)
    parser.add_argument("MUTATION",  help = "Values between 0 and 1000", type = check_mutation)
    parser.add_argument("GENERATIONS",  help = "Values between 1 and 100000", type = check_generations)
    parser.add_argument("INITIALIZATION",  help = "Values must be 0 or 1", type = check_initialization)
    parser.add_argument("STRATEGY",  help = "Values must be between 0 and 2", type = check_strategy)

    return parser.parse_args()

################################################################################

if __name__ == "__main__":
    args            = check_args()

    dim             = args.DIMENSIONS
    nb_organisms    = args.ORGANISMS
    nb_queens       = args.QUEENS
    nb_cpu          = args.CPUS
    mutation        = args.MUTATION
    nb_generations  = args.GENERATIONS
    initialization  = args.INITIALIZATION
    strategy        = args.STRATEGY

    with Pool(processes = nb_cpu) as pool:
        num = 1

        for _ in range(0, nb_cpu):
            _args           = (num, dim, nb_organisms, nb_queens, mutation, nb_generations, initialization, strategy)
            terminate_args  = partial(terminate, dim = dim, pool = pool)
            num             += 1

            pool.apply_async(search_queens, args = _args, callback = terminate_args)

        pool.close()
        pool.join()

################################################################################
