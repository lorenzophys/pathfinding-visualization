from settings import *


class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.f = 0
        self.g = 0
        self.h = 0
        self.previous = None
        self.neighbors = []
        self.is_wall = False
            

    def get_neighbors(self, grid):
        #There's probably a better way to do this
        row = self.row
        col = self.col
        if row+1 < N:
            right = grid[col][row+1]
            self.neighbors.append(right)
        if row > 0:
            left = grid[col][row-1]
            self.neighbors.append(left)
        if col+1 < N:
            up = grid[col+1][row]
            self.neighbors.append(up)
        if col > 0:
            down = grid[col-1][row]
            self.neighbors.append(down)
        #if row > 0 and col > 0:
        #    diag1 = grid[col-1][row-1]
        #    self.neighbors.append(diag1)
        #if col+1 < N and row > 0:
        #    diag2 = grid[col+1][row-1]
        #    self.neighbors.append(diag2)
        #if col > 0 and row+1 < N:
        #    diag3 = grid[col-1][row+1]
        #    self.neighbors.append(diag3)
        #if col+1 < N and row+1 < N:
        #    diag4 = grid[col+1][row+1]
        #    self.neighbors.append(diag4)


