import numpy as np


SIZES = [2, 3, 4, 5, 6, 7, 8]
MOVES_INPUT = dict(I="up", K="down", J="left", L="right", i="up", k="down", j="left", l="right")
UPPERBOUD = "upperbound"
LOWERBOUND = "lowerbound"
EXACT = "exact"
DIR = [[0,1],[]]
flag = 0
PLAYER_MOVES = ["left","down","right","up"]
#PLAYER_MOVES = ["right","down","left","up"]
'''PLAYER_NEXT_MOVE = {"left":["left","down","right","up","left","down","right","up"], \
                     "down":["down","right","up","left","up","left","down","right"], \
                    "right":["right","up","left","down","right","up","left","down"],  \
                       "up":["up","left","down","right","down","right","up","left"]} ''' 

PLAYER_NEXT_MOVE = {"left":["left","up","right","down","left","down","right","up"], \
                     "down":["down","left","up","right","up","left","down","right"], \
                    "right":["right","down","left","up","right","up","left","down"],  \
                       "up":["up","right","down","left","down","right","up","left"]} 
VALID_PLAYER_MOVES = {"left":["up","down"], "right":["up","down"], "up":["left","right"],"down":["left","right"]}
INVALID_PLAYER_MOVES = {"left":"right", "right":"left", "up":"down","down":"up",None:None}
def GAME_MOVES(board):
    empty_cells = board.empty_cells
    length = len(empty_cells[0])
    if (flag == 0):#allowed to place two or four
        values = [4]*length+[2]*length
        empty_cells = list(empty_cells)
        empty_cells[0] = list(empty_cells[0])*2
        empty_cells[1] = list(empty_cells[1])*2
        return zip(empty_cells[0], empty_cells[1], values)
    else:#only allowed to place 2
        values = [2]*len(empty_cells)
        return zip(empty_cells[0], empty_cells[1], values)
METHODS = ["minmax search", "alpha beta pruning", "iterative deepening"]

tiles = [2, 4, 8,  16, 32,  64,  128,  256,  512, 1024, 2048]
lower = [2, 4, 16, 48, 128, 320, 768, 1792, 4096, 9216, 20480]
upper = [2, 8, 24, 64, 160, 384, 896, 2048, 4608, 10240, 22528]