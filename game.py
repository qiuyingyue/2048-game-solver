import numpy as np
import csv
from board import Board2048
from initial_states import InitialStates
from GLOBAL import PLAYER_MOVES, METHODS,GAME_MOVES,MOVES_INPUT
import time, math
from minimax_search import minimax_alphabeta_moves, minimax_alphabeta_itdeepening,minimax_alphabeta
import time
class Game2048:
    """
    Abstraction of the 2048 game.

    Paramters
    ---------
    size : int in [2, 4, 8],  
        Size of game board.
    player_mode : string in ["human", "ai"],  
        Specifies whether the solver is human or ai.
    game_mode : string in ["human", "ai"],  
        Specifies whether the computer is random or ai.
    """
    def __init__(self, initial_grid, player_mode, game_mode, method_idx, play_turn=True):
        
        self.board = Board2048(grid=initial_grid,player_turn=play_turn,score=0)
        self.player_mode = player_mode
        self.game_mode = game_mode
        self.method = METHODS[method_idx]
        print(self.board)

    def generate_tile(self):
        empty_cells = self.board.empty_cells
        pos = np.random.randint(len(empty_cells[0]))
        if np.random.random() > 0.5:
            value = 4
        else:
            value = 2
        return (empty_cells[0][pos],empty_cells[1][pos]), value
    def input_move(self):
        move_char = input("Enter next move:")
        while (move_char not in MOVES_INPUT):
            print ("invalid move")
            move_char = input("Enter next move:")
        return MOVES_INPUT[move_char]

    def select_move(self, method):
        depth = 50000
        if method == "alpha beta pruning":
            if (self.board.player_turn):
                return minimax_alphabeta_moves(self.board, depth)
            else:
                return minimax_alphabeta_moves(self.board, depth-1)
        elif method == 'iterative deepening':
            return minimax_alphabeta_itdeepening(self.board, 100)
 


    def play(self):
        """Play game."""
        start = time.time()
        steps=0
        while(True):
            if(self.board.is_ended):#Game over
                break
            if (self.board.player_turn):
                steps+=1
                if (self.player_mode == "human"):
                    move = self.input_move()
                    
                elif (self.player_mode == "ai"):
                    move = self.select_move(self.method)
                print ("move:",move)
                self.board = self.board.slide(move)
            else:
                if (self.game_mode == "random"):
                    pos, value = self.generate_tile()
                    print ("move:",pos, value)
                elif (self.game_mode == "ai"):
                    move = self.select_move(self.method)
                    pos = (move[0], move[1])
                    value = move[2]#1#2
                    print ("move:",move)
                self.board = self.board.place(pos, value)
                print ("********************************")
                print(self.board)
                    
        print ("********************************")
        print ("Game over! Your score is {} . Max value achieved: {}".format(self.board.score,self.board.max_val))
        print ("Total number of moves for player:{}, time:{} seconds per move".format(steps,(time.time()-start)/steps))
        print ("player mode {}, game mode {}".format(self.player_mode,self.game_mode))
        return self.board, steps 
             


if __name__ == "__main__":
   

    '''empty_grid = np.zeros((3,2))
    empty_grid[0][0]=2
    empty_grid[0][1]=2
    #Game2048(empty_grid, "human","ai",method_idx=1).play()
    board = Board2048(grid=empty_grid, player_turn=True,score=0)
    print (board)
    minimax_alphabeta_moves(board, 3000000)

    empty_grid = np.zeros((3,3))
    empty_grid[0][0]=2
    empty_grid[0][1]=2
    #Game2048(empty_grid, "human","ai",method_idx=1).play()
    board = Board2048(grid=empty_grid, player_turn=True,score=0)
    print (board)
    minimax_alphabeta_moves(board, 3000000)


    empty_grid = np.zeros((3,2))
    empty_grid[2][0]=2
    empty_grid[2][1]=4
    board = Board2048(grid=empty_grid, player_turn=True,score=0)
    print (board)    
    minimax_alphabeta_moves(board, 3000000)

    empty_grid[2][0]=4
    empty_grid[2][1]=2
    board = Board2048(grid=empty_grid, player_turn=True,score=0)
    print (board)
    minimax_alphabeta_moves(board, 3000000)
    empty_grid[0][0]=256
    empty_grid[0][1]=128
    empty_grid[0][2]=64
    empty_grid[1][0]=8
    empty_grid[1][1]=16
    empty_grid[1][2]=32
    empty_grid[2][0]=4
    empty_grid[2][1]=0
    empty_grid[2][2]=0'''
    '''empty_grid[0][0]=2
    empty_grid[0][1]=4
    empty_grid[0][2]=128
    empty_grid[1][0]=16
    empty_grid[1][1]=32
    empty_grid[1][2]=4
    empty_grid[2][0]=4  
    empty_grid[2][1]=4
    empty_grid[2][2]=8
    Game2048(3, empty_grid, "ai","random", method_idx=2).play()'''

    choice = int(input("Please specify the size of the game: 1:2*2, 2:2*3, 3:3*2, 4:3*3, 5:3*4, 6:4*3, 7:4*4\n"))
    choice_dict = {1:(2,2), 2:(2,3), 3:(3,2), 4:(3,3), 5:(3,4), 6:(4,3), 7:(4,4)}
    shape = choice_dict[int(choice)]
    initial_grid_list = InitialStates(shape).generate()
    csvfile = open("log_size{0}*{1}_24.csv".format(shape[0],shape[1]), "w")
    writer = csv.writer(csvfile)
    writer.writerow(['initial state','end state','score','max value','time', 'number of nodes'])
    i = 0
    for initial_grid in initial_grid_list:#[58:59]: #58 True 10 false
        i+=1
        print ("############################################ New Game ##################################################",i)  
        
        board = Board2048(grid=initial_grid,player_turn=True,score=0)
        depth_limit = 50000
        trans_table = {}
        start = time.time()
        best_val,d,best_move,end_board = minimax_alphabeta(board, depth_limit, depth_limit, -math.inf, math.inf, trans_table, {}, node_ordering=True)
        print ("Return the result of depth {}: selected move {} with value {}".format(d, best_move, best_val)) 
        print ("depth:{}, total nodes:{}, current nodes:{}. value:{}, move:{}, d:{}, size of table:{}".format(depth_limit,cnt_nodes,cnt_nodes_it,best_val,best_move,d,len(trans_table)))
        print ("end state{}, is_complete{}".format(end_board, is_complete))
       
        #end_board, steps = Game2048(initial_grid, "ai","ai",method_idx=2).play()
        writer.writerow([board, end_board, end_board.score, end_board.max_val, end_board.sum_val, time.time()-start, cnt_nodes])