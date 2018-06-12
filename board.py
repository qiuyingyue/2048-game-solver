
import numpy as np
from GLOBAL import PLAYER_MOVES, METHODS,GAME_MOVES

import math


class Board2048(object):
    """
    Abstraction of the 2048 game board.

    Paramters
    ---------
    size : int in [2, 4, 8], optional (default None)
        Size of game board.

    grid : 2D array of shape (size, size), optional (default None)
        Values to initialize game board (useful for cloning game instances)

    

    mover : callable, optional (default None)
        Returns next move to be made. If none, next moves will asked at the
        stdin as game play proceeds.
    """

    def __init__(self, grid, player_turn, score):
        
        self.size = grid.shape[0] * grid.shape[1]
        
        self.player_turn = player_turn
        self.grid_ = grid
        self.score = score
        
    def get_params(self):
        """Get all parameters of class instance."""
        return dict(grid=self.grid_.copy())

    def clone(self):
        """Clone class instance."""
        return Board2048(**self.get_params())

    def __hash__(self):
        return hash((str(self.grid_), self.player_turn))

    def __eq__(self, other):

        """Compare game board with another instance."""
        #return ((self.grid_ == other.grid_) | (np.isnan(self.grid_) & np.isnan(other.grid_))).all()
        return np.all(self.grid_ == other.grid_) and self.player_turn == other.player_turn

    def __ne__(self, other):
        """Compare game board with another instance."""
        return np.any(self.grid_ != other.grid_) or self.player_turn != other.player_turn

    def place(self, pos, value):
        """return a new board instance after placing a new tile"""
        if(self.player_turn):
            print("invalid board: board.py line 68")
        newgrid = np.copy(self.grid_)
        newgrid[pos[0]][pos[1]] = int(value)
        '''if (int(value)==2):
            score = self.score
        else:
            score = self.score + 4'''
        return Board2048(newgrid, True, self.score)

    def slide(self, move, fake = False):
        """return a new board instance after the player move"""
        if(not self.player_turn):
            print("invalid board: board.py line 76")
        if move == "up":
            newgrid, score_added = self._horizontal_move(self.grid_.T)
            newgrid = newgrid.T
        elif move == "down":
            oldgrid = np.flip(self.grid_.T, axis = 1)
            newgrid, score_added = self._horizontal_move(oldgrid)
            newgrid = np.flip(newgrid, axis = 1).T
        elif move == "left":
            newgrid, score_added = self._horizontal_move(self.grid_)
        elif move == "right":
            oldgrid = np.flip(self.grid_, axis=1)
            newgrid, score_added = self._horizontal_move(oldgrid)
            newgrid = np.flip(newgrid, axis=1)
        else:
            newgrid = self.grid_
            score_added = 0
            print("invalid move: board.py line 93")
        if (score_added < 0):
            print ("score error: board.py line 95")
        return Board2048(newgrid, fake, self.score + score_added)
        


    '''def _horizontal_move(self, oldgrid):
        """helper function for moving left"""
        newgrid = []
        llen = self.size
        score_added = 0
        for line in oldgrid:
            i=0
            j=0
            flag = [False]*llen
            newline = np.empty(llen)
            newline.fill(math.nan)
            while (j<llen):
                if (math.isnan(line[j])):
                    j+=1
                    continue
                if (newline[i]==line[j] and not flag[i]):
                    newline[i] += 1
                    score_added += 2**newline[i]
                    i+=1
                else:
                    if (not math.isnan(newline[i])):
                        i+=1
                    newline[i] = line[j]
                j+=1
            #print("line:",line,",newline:",newline)
            newgrid.append(newline)
                
        newgrid = np.array(newgrid)
        #print ("newgrid:\n",newgrid)
        return newgrid, score_added'''
    def _horizontal_move(self, oldgrid):
        """helper function for moving left"""
        newgrid = []
        llen = oldgrid.shape[1]#self.size
        score_added = 0
        for line in oldgrid:
            i=0
            j=0
            newline = np.zeros(llen)
            while (j<llen):
                if (line[j]==0):
                    j+=1
                    continue
                if (newline[i]==line[j] ):
                    newline[i] *= 2
                    score_added += newline[i]
                    i+=1
                else:
                    if (newline[i]!=0):
                        i+=1
                    newline[i] = line[j]
                j+=1
            #print("line:",line,",newline:",newline)
            newgrid.append(newline)
                
        newgrid = np.array(newgrid)
        #print ("newgrid:\n",newgrid)
        return newgrid, score_added
    

   
    def generate_sym(self):
        """generate all the sysmetric boards"""
        shape = self.grid_.shape
        mirror = np.flip(self.grid_, axis = 0)
        #move_matrix = np.zeros(self.grid_.shape)
        #move_matrix[move[0]][move[1]]=move[2]
        if (shape[0]!=shape[1]):
            step = 2
        else:
            step = 1
        for i in range(0, 8, step):
            if (int(i/4) == 0):
                grid = self.grid_
            else:
                grid = mirror
            newgrid = np.rot90(grid, i%4)#counter clockwise
            yield Board2048(newgrid, self.player_turn, self.score)
            #blist.append(Board2048(newgrid, self.player_turn, self.score))
        #return blist


    @property
    def empty_cells(self):
        #return np.where(self.grid_))
        return np.where(self.grid_==0)

    @property
    def max_val(self):
        #return 2**np.max(self.grid_)
        return np.max(self.grid_)

    @property
    def sum_val(self):
        #return np.nansum(2**self.grid_)
        return np.sum(self.grid_)

    @property
    def zero_counts(self):
        return self.grid_.size - self.nonzero_counts        
        #return np.count_nonzero(np.isnan(self.grid_))

    @property
    def nonzero_counts(self):
        return np.count_nonzero(self.grid_)
        #return self.grid_.size - self.zero_counts
    @property
    def is_empty(self):
        return np.all(self.grid_ == 0)
    @property
    def is_full(self):
        """Check whether grid is full."""
        return np.all(self.grid_ != 0)
        #return ~np.any(np.isnan(self.grid_))
    def is_same(self, other):
        return np.all(self.grid_ == other.grid_)
    @property
    def is_ended(self):
        if not self.is_full:
            return False
        elif self.player_turn:
            for move in PLAYER_MOVES:
                if not self.slide(move).is_same(self):
                    return False
        if (not self.player_turn):
            print("board.py 202 end")
        return True
        #return self.is_full and (not self.player_turn)
    def __repr__(self):
        """Converts "2048" board to a string."""
        out = ""
        line = None
        for line in [[(str(int(x)) if x!=0 else "").center(6) + "|" for x in line]#not math.isnan(x)
                     for line in self.grid_]:
            line = "|%s" % "".join(line)
            out += "%s\n" % line
            out += "%s\n" % ("-" * len(line))
        out = "%s\n%s" % ("-" * len(line), out)
        out += "score:{} player turn:{}".format(self.score, self.player_turn)

        return out




