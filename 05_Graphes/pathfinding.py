# Copyright © 2025 Charles Theetten
# Tous droits réservés.
# Ce programme est distribué sous licence CC BY-NC-ND 4.0.

################################################################################

# pylint: disable=C0301, R0902, R0903

################################################################################

""" pathfinding """

################################################################################

import  random
import  time
import  tkinter     as tk

from    collections import deque
from    heapq       import heappop
from    heapq       import heappush
from    tkinter     import ttk

################################################################################

class ECell:
    """ ECell class """
    EMPTY   = -1
    START   = 0
    END     = 1
    PATH    = 2
    WALL    = 3

################################################################################

class Cell:
    """ Cell class """
    def __init__(self, kind, x, y, distance):
        """ constructor """
        self.kind       = kind
        self.x          = x
        self.y          = y
        self.distance   = distance
        self.weight     = 1
        self.visited    = False
        self.adj_cells  = []

    def __eq__(self, other):
        """ _eq_ method """
        if self is other:
            return True
        if other is None:
            return False
        if self.__class__ != other.__class__:
            return False

        return self.x == other.x and self.y == other.y

    def __str__(self):
        """ __str__  function """
        return f"({self.x}, {self.y})"

    def __lt__(self, other):
        """ __lt__ function """
        return self.distance < other.distance

################################################################################

class Maze:
    """ Maze class """
    def __init__(self, width, height, density):
        """ constructor """
        self.width  = width
        self.height = height
        self.data   = self.init_maze(width, height, density)
        self.start  = None
        self.end    = None
        self.path   = []

    ################################################################################

    def init_maze(self, width, height, density):
        """ init_maze function """
        data = []

        for i in range(height):
            row = []

            for j in range(width):
                if density == 0:
                    row.append(Cell(ECell.PATH, i, j, float("inf")))
                else:
                    if random.random() < density:
                        row.append(Cell(ECell.WALL, i, j, -1))
                    else:
                        row.append(Cell(ECell.EMPTY, i, j, float("inf")))

            data.append(row)

        return data

    ################################################################################

    def bfs(self):
        """ bfs function """
        cell    = self.start
        queue   = deque([ cell ])

        while queue:
            cell = queue.popleft()

            if cell != self.end:
                self.path.append((cell.x, cell.y))
                for adj_cell in cell.adj_cells:
                    if not adj_cell.visited:
                        adj_cell.visited = True
                        queue.append(adj_cell)
            else:
                break

        return cell == self.end

    ################################################################################

    def dfs(self):
        """ dfs function """
        cell    = self.start
        stack   = [ cell ]

        while stack:
            cell = stack.pop()
            if cell != self.end:
                self.path.append((cell.x, cell.y))
                for adj_cell in cell.adj_cells:
                    if not adj_cell.visited:
                        adj_cell.visited = True
                        stack.append(adj_cell)
            else:
                break

        return cell == self.end

    ################################################################################

    def dijkstra_search(self):
        """ dijkstra_search function """
        cell    = self.start
        queue   = [ (cell.distance, cell) ]

        while queue:
            _, cell = heappop(queue)

            for adj_cell in cell.adj_cells:
                adj_cell.distance = min(adj_cell.distance, cell.distance + adj_cell.weight)
                if not adj_cell.visited:
                    heappush(queue, (adj_cell.distance, adj_cell))
                    adj_cell.visited = True

        self.build_path()

        return self.end.visited

    ################################################################################

    def build_path(self):
        """ build_path function """
        if self.end.visited:
            cell = self.end

            while cell != self.start:
                self.path.append((cell.x, cell.y))
                min_cell    = min(cell.adj_cells, key = lambda c: c.distance)
                cell        = min_cell

        self.path.reverse()

    ################################################################################

    def set_adjacent_cells(self):
        """ set_adjacent_cells function """
        for i in range(self.height):
            for j in range(self.width):
                cell = self.data[i][j]

                if i > 0 and self.data[i - 1][j].kind != ECell.WALL:
                    cell.adj_cells.append(self.data[i - 1][j])
                if i < self.height - 1 and self.data[i + 1][j].kind != ECell.WALL:
                    cell.adj_cells.append(self.data[i + 1][j])
                if j > 0 and self.data[i][j - 1].kind != ECell.WALL:
                    cell.adj_cells.append(self.data[i][j - 1])
                if j < self.width - 1 and self.data[i][j + 1].kind != ECell.WALL:
                    cell.adj_cells.append(self.data[i][j + 1])

################################################################################

class PathFinding:
    """ PathFinding class """
    def __init__(self, root):
        """ constructor """
        self.root = root
        self.root.title("PathFinding")

        screen_width    = self.root.winfo_screenwidth()
        screen_height   = self.root.winfo_screenheight()

        window_width    = screen_width // 2
        window_height   = (screen_height * 2) // 3

        self.root.geometry(f"{window_width}x{window_height}+{screen_width//4}+{screen_height//6}")
        self.root.resizable(False, False)

        menu_width      = int(window_width * 0.15)
        self.menu_frame = tk.Frame(root, width = menu_width, bg = "black")
        self.menu_frame.pack(side = "left", fill = "y")

        self.add_menu_widgets()

        self.canvas = tk.Canvas(root, bg = "#2E4053")
        self.canvas.pack(side = "right", fill = "both", expand = True)

        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.maze       = None
        self.num_cols   = 0
        self.num_rows   = 0
        self.cells      = {}

    ################################################################################

    def add_menu_widgets(self):
        """ add_menu_widgets function """
        tk.Button(self.menu_frame, text = "Init", command = self.init_grid).pack(pady = 10, padx = 10, fill = "x")
        tk.Button(self.menu_frame, text = "Solve", command = self.solve_maze).pack(pady = 10, padx = 10, fill = "x")

        self.path_label = tk.Label(self.menu_frame, text = "Chemin")
        self.path_label.pack(pady = 10, padx = 10, fill = "x")

        self.path_length_label = tk.Label(self.menu_frame, text = "0")
        self.path_length_label.pack(pady = 10, padx = 10, fill = "x")

        tk.Label(self.menu_frame, text = "Taille du labyrinthe :", bg = "black", fg = "white").pack(pady = 10, padx = 10, fill = "x")
        self.size_scale = tk.Scale(self.menu_frame, from_ = 0, to = 4, orient = tk.HORIZONTAL, command = self.update_size_label)
        self.size_scale.pack(pady = 10, padx = 10, fill = "x")
        self.size_scale.set(0)
        self.size_values    = [10, 25, 50, 100, 250]
        self.size_label     = tk.Label(self.menu_frame, text = str(self.size_values[0]), bg = "black", fg = "white")
        self.size_label.pack(pady = 10, padx = 10, fill = "x")

        tk.Label(self.menu_frame, text = "Densité :").pack(pady = 10, padx = 10, fill = "x")
        self.density_scale = tk.Scale(self.menu_frame, from_ = 0, to = 1, resolution = 0.1, orient = tk.HORIZONTAL)
        self.density_scale.pack(pady = 10, padx = 10, fill = "x")
        self.density_scale.set(0.3)

        tk.Label(self.menu_frame, text = "Algorithmes :").pack(pady = 10, padx = 10, fill = "x")
        self.algorithm_combobox = ttk.Combobox(self.menu_frame, values = [ "DFS", "BFS", "DIJKSTRA" ])
        self.algorithm_combobox.pack(pady = 10, padx = 10, fill = "x")
        self.algorithm_combobox.set("DFS")

        tk.Label(self.menu_frame, text = "Cases :").pack(pady = 10, padx = 10, fill = "x")
        self.cases_combobox = ttk.Combobox(self.menu_frame, values = [ "Start", "End", "Path", "Wall" ])
        self.cases_combobox.pack(pady = 10, padx = 10, fill = "x")
        self.cases_combobox.set("Start")

        tk.Label(self.menu_frame, text = "Délai de dessin :").pack(pady = 10, padx = 10, fill = "x")
        self.delay_scale = ttk.Combobox(self.menu_frame, values = [ 1, 0.1, 0.01, 0.001 ])
        self.delay_scale.pack(pady = 10, padx = 10, fill = "x")
        self.delay_scale.set(0.1)

        tk.Button(self.menu_frame, text = "Draw", command = self.draw_path).pack(pady = 10, padx = 10, fill = "x")

    ################################################################################

    def update_size_label(self, val):
        """ update_size_label function """
        self.size_label.config(text = str(self.size_values[int(val)]))

    ################################################################################

    def init_grid(self):
        """ init_grid function """
        try:
            grid_size   = self.size_values[int(self.size_scale.get())]
            density     = self.density_scale.get()
            self.maze   = Maze(grid_size, grid_size, density)
            self.maze.set_adjacent_cells()
        except ValueError:
            grid_size   = 20

        self.num_cols = grid_size
        self.num_rows = grid_size

        self.draw_grid()

    ################################################################################

    def draw_grid(self):
        """ draw_grid function """
        self.canvas.delete("all")

        self.cells      = {}
        canvas_width    = self.canvas.winfo_width()
        canvas_height   = self.canvas.winfo_height()
        cell_width      = canvas_width / self.num_cols
        cell_height     = canvas_height / self.num_rows

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                x1      = i * cell_width
                y1      = j * cell_height
                x2      = x1 + cell_width
                y2      = y1 + cell_height
                cell    = self.canvas.create_rectangle(x1, y1, x2, y2, fill = "#2E4053", outline = "black")

                self.cells[ (i, j) ] = cell

                if self.maze.data[j][i].kind == ECell.WALL:
                    self.canvas.itemconfig(cell, fill = "black")
                elif self.maze.data[j][i].kind == ECell.START:
                    self.canvas.itemconfig(cell, fill = "aqua")
                elif self.maze.data[j][i].kind == ECell.END:
                    self.canvas.itemconfig(cell, fill = "lime")
                elif self.maze.data[j][i].kind == ECell.PATH:
                    self.canvas.itemconfig(cell, fill = "fuchsia")

    ################################################################################

    def draw_path(self):
        """ draw_path function """
        delay = float(self.delay_scale.get())

        for (x, y) in self.maze.path:
            cell = self.cells.get((y, x))

            if cell:
                self.canvas.itemconfig(cell, fill = "fuchsia")

            self.canvas.update()
            time.sleep(delay)

    ################################################################################

    def on_canvas_resize(self, _event):
        """ on_canvas_resize function """
        self.draw_grid()

    ################################################################################

    def on_canvas_click(self, event):
        """ on_canvas_click function """
        cell_width  = self.canvas.winfo_width() / self.num_cols
        cell_height = self.canvas.winfo_height() / self.num_rows
        x           = int(event.x / cell_width)
        y           = int(event.y / cell_height)
        cell        = self.cells.get((x, y))

        if cell:
            case_kind = self.cases_combobox.get()
            if case_kind == "Start":
                new_color                   = "aqua"
                self.maze.start             = self.maze.data[y][x]
                self.maze.start.kind        = ECell.START
                self.maze.start.visited     = True
                self.maze.start.distance    = 0
                self.cases_combobox.set("End")
            elif case_kind == "End":
                new_color                   = "lime"
                self.maze.end               = self.maze.data[y][x]
                self.maze.end.kind          = ECell.END
                self.cases_combobox.set("Start")
            elif case_kind == "Wall":
                new_color                   = "black"
                self.maze.data[y][x].kind   = ECell.WALL
            elif case_kind == "Path":
                new_color                   = "fuchsia"
                self.maze.data[y][x].kind   = ECell.PATH
            else:
                new_color                   = "white"

            self.canvas.itemconfig(cell, fill = new_color)

    ################################################################################

    def solve_maze(self):
        """ solve_maze function """
        algorithm = self.algorithm_combobox.get()

        if algorithm == "DFS":
            self.maze.dfs()
        elif algorithm == "BFS":
            self.maze.bfs()
        elif algorithm == "DIJKSTRA":
            self.maze.dijkstra_search()

        if self.maze.path:
            if self.maze.path[0] == (self.maze.start.x, self.maze.start.y):
                self.maze.path.pop(0)
            if self.maze.path[-1] == (self.maze.end.x, self.maze.end.y):
                self.maze.path.pop()

        if self.maze.end.visited:
            self.path_length_label.config(text = str(len(self.maze.path)))
        else:
            self.path_length_label.config(text = "-1")

################################################################################

def main():
    """ main function """
    root    = tk.Tk()

    PathFinding(root)
    root.mainloop()

################################################################################

if __name__ == "__main__":
    main()

################################################################################
