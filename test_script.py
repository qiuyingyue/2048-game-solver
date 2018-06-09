
from board import Board2048
import numpy as np
from initial_states import InitialStates
def generate_sym(self):
    """generate all the sysmetric boards"""
    mirror = np.flip(self.grid_, axis = 0)
    #move_matrix = np.zeros(self.grid_.shape)
    #move_matrix[move[0]][move[1]]=move[2]
    for i in range(8):
        if (int(i/4) == 0):
            grid = self.grid_
        else:
            grid = mirror
        newgrid = np.rot90(grid, i%4)#counter clockwise
        yield Board2048(newgrid, self.player_turn, self.score)
grid = InitialStates((3,2)).generate()[58]
board = Board2048(grid=grid,player_turn=True,score=0)
for a in generate_sym(board):
    print (a)