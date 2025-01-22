# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

# pylint: disable=C0301, C0200, E0611, E1101, R0902

""" Game of Life """

################################################################################

import  argparse
import  numpy           as np
import  pygame          as pg

from    scipy.signal    import convolve2d

################################################################################

WHITE = pg.Color(255, 255, 255)

################################################################################

class Gol():
    """ Gol class """

    ############################################################################

    def __init__(self, dim, random, delay, pattern):
        """ init function """
        pg.display.init()

        self.screen_height  = (pg.display.Info().current_h * 2) // 3
        self.screen_width   = self.screen_height * 2
        self.dim            = dim
        self.width          = self.screen_height // dim
        self.random         = random
        self.delay          = delay
        self.running        = False
        self.start          = 0
        self.grid           = np.zeros((dim, dim * 2))
        self.new_grid       = np.zeros((dim, dim * 2))
        self.image          = np.zeros((dim, dim * 2))
        self.surface        = pg.Surface((dim * 2, dim))
        self.screen         = pg.display.set_mode((self.screen_width, self.screen_height), 0, 32)

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
            with open(pattern, encoding = "utf-8") as f:
                contents    = f.readlines()
                m           = len(max(contents, key = len))
                n           = len(contents)
                i           = self.dim // 2 - n // 2
                j           = self.dim      - m // 2

                for line in contents:
                    for c in line:
                        if c == "O":
                            self.grid[i][j] = 1
                        j += 1
                    i += 1
                    j = self.dim - m // 2

                self.image = self.grid * int(WHITE)

    ############################################################################

    def update(self):
        """ update function """
        kernel          = np.ones((3, 3), dtype = int)
        kernel[1, 1]    = 0
        self.new_grid   = convolve2d(self.grid, kernel, mode = "same", boundary = "fill", fillvalue = 0)
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
        surface = pg.transform.scale(self.surface, (self.screen_width, self.screen_height))

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

def check_dimensions(value):
    """ check_dimensions function """
    dimensions = int(value)

    if dimensions not in [ 5, 10, 50, 100, 500, 1000 ]:
        raise argparse.ArgumentTypeError(f"DIMENSIONS must be in [ 5, 10, 50, 100, 500, 1000 ], got {dimensions}.")

    return dimensions

def check_random(value):
    """ check_random function """
    random = float(value)

    if random not in np.arange(0, 1.1, 0.01):
        raise argparse.ArgumentTypeError(f"RANDOM must be between 0 and 1, got {random}.")

    return random

def check_delay(value):
    """ check_delay function """
    delay = int(value)

    if delay not in np.arange(1, 10001, 1):
        raise argparse.ArgumentTypeError(f"DELAY must between 1 and 10000, got {delay}.")

    return delay

def check_args():
    """ check_args function """
    parser = argparse.ArgumentParser()

    parser.add_argument("DIMENSIONS", help = "Values in {5, 10, 50, 100, 500, 1000}.", type = check_dimensions)
    parser.add_argument("RANDOM",  help = "Values in {0... 1}.", type = check_random)
    parser.add_argument("DELAY",  help = "Values in {1... 10000}.", type = check_delay)
    parser.add_argument("FILE",  help = "File name.", type = str, nargs = "?", default = "")

    return parser.parse_args()

################################################################################

def main():
    """ main function"""
    args    = check_args()

    dim     = args.DIMENSIONS
    random  = args.RANDOM
    delay   = args.DELAY
    pattern = args.FILE

    gol     = Gol(dim, random, delay, pattern)
    gol.run()

    pg.quit()

################################################################################

if __name__ == '__main__':
    main()

################################################################################
