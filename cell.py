from window import Point, Line

class Cell:
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window
        

    def draw(self, x1, y1, x2, y2):
        if self.__win is None:
            return

        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__win.draw_line(line, "white")

        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__win.draw_line(line)
        else:  
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__win.draw_line(line, "white")
        
        
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__win.draw_line(line)
        else:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__win.draw_line(line, "white")

        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__win.draw_line(line)
        else:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__win.draw_line(line, "white")
         
    def draw_move(self, to_cell, undo=False):
        color = "red"
        if undo:
            color = "gray"

        x1 = (self.__x1 + self.__x2)//2
        y1 = (self.__y1 + self.__y2)//2
        x2 = (to_cell.__x1 + to_cell.__x2)//2
        y2 = (to_cell.__y1 + to_cell.__y2)//2
        
        line = Line(Point(x1,y1), Point(x2,y2))

        self.__win.draw_line(line, color)