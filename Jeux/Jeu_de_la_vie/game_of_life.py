# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

# pylint: disable=C0301, C0200, E0611, E1101, R0902

""" Game of Life """

################################################################################

import  argparse
import  sys
import  numpy           as np
import  pygame          as pg

from    scipy.signal    import convolve2d

################################################################################

WHITE           = pg.Color(255, 255, 255)

SCREEN_WIDTH    = 2000
SCREEN_HEIGHT   = 1000

################################################################################

class Gol():
    """ Gol class """

    ############################################################################

    def __init__(self, dim, random, delay, pattern):
        """ init function """
        self.dim        = dim
        self.width      = SCREEN_HEIGHT // dim
        self.random     = random
        self.delay      = delay
        self.running    = False
        self.start      = 0
        self.grid       = np.zeros((dim, dim * 2))
        self.new_grid   = np.zeros((dim, dim * 2))
        self.image      = np.zeros((dim, dim * 2))
        self.surface    = pg.Surface((dim * 2, dim))
        self.screen     = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

        self.init_pygame()
        self.init_grid(pattern)
        self.draw_grid()

    ############################################################################

    def init_pygame(self):
        """ init_pygame function """
        pg.init()
        pg.display.set_caption("Game of Life")
        pg.display.update()

    ############################################################################

    def init_cell(self, x, y, p):
        """ init_cell function """
        self.grid[x][y] = 1 if p == 1 else 0

    ############################################################################

    def init_grid(self, pattern):
        """ init_grid function """
        if pattern == "":
            self.grid   = np.random.choice([0, 1], size = self.grid.shape, p = [1 - self.random, self.random])
            self.image  = self.grid * int(WHITE)
        else:
            with open(pattern) as f:
                contents    = f.readlines()
                m           = len(max(contents, key = len))
                n           = len(contents)
                i           = self.dim // 2 - n // 2
                j           = self.dim      - m // 2

                for line in contents:
                    for c in line:
                        if c == "\n":
                            break
                            i += 1
                        elif c == "O":
                            self.grid[i][j] = 1
                        j += 1
                    i += 1
                    j = self.dim      - m // 2

                self.image = self.grid * int(WHITE)

    ############################################################################

    def update(self):
        """ update function """
        self.new_grid   = convolve2d(self.grid, np.ones((3, 3), dtype = int), "same") - self.grid
        self.new_grid   = ((self.new_grid == 3) | ((self.grid == 1) & (self.new_grid == 2))).astype(int)
        self.image      = self.new_grid * int(WHITE)
        self.grid       = self.new_grid
        self.new_grid   = np.zeros((self.dim, self.dim * 2))

    ############################################################################

    def inputs(self):
        """ inputs function """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.start = True
                if event.key == pg.K_p:
                    self.start ^= 1
                if event.key == pg.K_r:
                    self.start = False
                    self.init_grid("")
                if event.key == pg.K_SPACE:
                    self.running = False
        
        if pg.mouse.get_pressed() == (True, False, False):
            pos = pg.mouse.get_pos()
            self.init_cell(pos[1] // self.width, pos[0] // self.width, 1)
            self.image = self.grid * int(WHITE)
        elif pg.mouse.get_pressed() == (False, False, True):
            pos = pg.mouse.get_pos()
            self.init_cell(pos[1] // self.width, pos[0] // self.width, 3)
            self.image = self.grid * int(WHITE)

    ############################################################################

    def draw_grid(self):
        """ draw_grid function """
        surface = pg.transform.scale(self.surface, (SCREEN_WIDTH, SCREEN_HEIGHT))

        pg.surfarray.blit_array(self.surface, self.image.transpose())
        self.screen.blit(surface, (0, 0))
        pg.display.update()

    ############################################################################

    def run(self):
        """ run function """
        self.running    = True
        start_time      = pg.time.get_ticks()

        while self.running:
            self.inputs()

            if pg.time.get_ticks() - start_time >= self.delay and self.start == 1:
                self.update()
                start_time = pg.time.get_ticks()

            self.draw_grid()

################################################################################

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("DIMENSIONS", help = "values in {5, 10, 20, 25, 50, 100, 150, 200, 300, 400, 500, 750, 1000}.", type = int)
    parser.add_argument("RANDOM",  help = "values in {0... 1}.", type = float)
    parser.add_argument("DELAY",  help = "values in {1... 10000}.", type = int)
    parser.add_argument("FILE",  help = "file name.", type = str, nargs = "?", default = "")

    args = parser.parse_args()

    try:
        if args.DIMENSIONS not in [5, 10, 20, 25, 50, 100, 150, 200, 300, 400, 500, 750, 1000]:
            raise argparse.ArgumentTypeError(f"DIMENSIONS : {args.DIMENSIONS} is an invalid value.")
        if args.RANDOM not in np.arange(0, 1.1, 0.01):
            raise argparse.ArgumentTypeError(f"RANDOM : {args.RANDOM} is an invalid value.")
        if args.DELAY not in np.arange(1, 10001, 1):
            raise argparse.ArgumentTypeError(f"DELAY : {args.DELAY} is an invalid value.")
        if args.FILE is None:
            args.FILE = ""

    except argparse.ArgumentTypeError as e:
        print(f"Argument Error - {e}\n")
        parser.print_help()
        pg.quit()
        sys.exit(-1)
    
    return args

################################################################################

def main():
    """ main function"""
    args    = check_args()

    dim     = int(sys.argv[1])
    random  = float(sys.argv[2])
    delay   = int(sys.argv[3])
    pattern = args.FILE

    gol     = Gol(dim, random, delay, pattern)
    gol.run()

    pg.quit()

################################################################################

if __name__ == '__main__':
    main()

################################################################################
