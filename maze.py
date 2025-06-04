from window import Point, Line
from cell import Cell
import time
import random

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None,
        ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells = []
        if seed != None:
            random.seed(seed)
        
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self):
        for i in range(self.__num_cols):
            self.__cells.append([])
            for j in range(self.__num_rows):
                cell = Cell(self.__win)
                self.__cells[i].append(cell)
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        x1 = self.__x1 + (self.__cell_size_x * i)
        y1 = self.__y1 + (self.__cell_size_y * j)
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        
        col = self.__num_cols-1
        row = self.__num_rows-1

        self.__cells[col][row].has_bottom_wall = False
        self.__draw_cell(col, row)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            possible_directions = []
            if i - 1 >= 0:
                if not self.__cells[i-1][j].visited:
                    possible_directions.append([i-1, j, "left"])
            if i + 1 < self.__num_cols:
                if not self.__cells[i+1][j].visited:
                    possible_directions.append([i+1, j, "right"])
            if j - 1 >= 0:
                if not self.__cells[i][j-1].visited:
                    possible_directions.append([i, j-1, "up"])
            if j + 1 < self.__num_rows:
                if not self.__cells[i][j+1].visited:
                    possible_directions.append([i, j+1, "down"])
            if len(possible_directions) == 0:
                self.__draw_cell(i,j)
                return
            direction = possible_directions[random.randrange(0, len(possible_directions))]
            
            if direction[2] == "left":
                self.__cells[i][j].has_left_wall = False
                self.__cells[direction[0]][direction[1]].has_right_wall = False
            elif direction[2] == "right":
                self.__cells[i][j].has_right_wall = False
                self.__cells[direction[0]][direction[1]].has_left_wall = False
            elif direction[2] == "up":
                self.__cells[i][j].has_top_wall = False
                self.__cells[direction[0]][direction[1]].has_bottom_wall = False
            else:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[direction[0]][direction[1]].has_top_wall = False
            
            self.__break_walls_r(direction[0], direction[1])

    def __reset_cells_visited(self):
        for col in self.__cells:
            for cell in col:
                cell.visited = False


    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self.__animate()
        current = self.__cells[i][j]
        current.visited = True
        if i == (self.__num_cols - 1) and j == (self.__num_rows - 1):
            return True
        if (
            i > 0 
            and not current.has_left_wall
            and not self.__cells[i-1][j].visited
            ):
            current.draw_move(self.__cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            current.draw_move(self.__cells[i-1][j], undo=True)
        
        if (
            i < self.__num_cols - 1 
            and not current.has_right_wall 
            and not self.__cells[i+1][j].visited
            ):
            current.draw_move(self.__cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            current.draw_move(self.__cells[i+1][j], undo=True)
        
        if (
            j > 0 
            and not current.has_top_wall 
            and not self.__cells[i][j-1].visited
            ):
            current.draw_move(self.__cells[i][j-1])
            if self._solve_r(i, j-1):
                return True
            current.draw_move(self.__cells[i][j-1], undo=True)

        if (
            j < (self.__num_rows - 1) 
            and not current.has_bottom_wall 
            and not self.__cells[i][j+1].visited
            ):
            current.draw_move(self.__cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            current.draw_move(self.__cells[i][j+1], undo=True)
                
        return False