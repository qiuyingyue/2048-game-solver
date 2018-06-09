from GLOBAL import PLAYER_MOVES, INVALID_PLAYER_MOVES
from board import Board2048
import numpy as np
def compute_monotonicity(grid):
    cnt_row = 0
    cnt_col = 0
    #horizontal diff
    diff_sign = np.sign(np.diff(grid, axis=0))
    for i in range(grid.shape[1]):
        sign_col = diff_sign[:,i]
        #penalty for non_monotonic
        if np.all(sign_col==1) or np.all(sign_col==-1):
            #penalty+=10*np.max(grid[:,i])
            cnt_row += np.sum(grid[:,i])
    diff_sign = np.sign(np.diff(grid, axis=1))
    for i in range(grid.shape[0]):
        sign_row = diff_sign[i]
        #penalty for non_monotonic
        if np.all(sign_row==1) or np.all(sign_row==-1):
            cnt_row += np.sum(grid[i])            
            #penalty+=10*np.max(grid[i])
    return  cnt_col + cnt_row
    
    
def compute_smoothness(grid):
    '''penalty=0
    # diff in each column
    diff = abs(np.diff(grid, axis=0))
    penalty+=np.nansum(abs(diff))
    # diff in each row
    diff = abs(np.diff(grid, axis=1))
    #diff = np.insert(diff,diff.shape[1],math.nan,axis = 1)
    penalty+=np.nansum(abs(diff))'''

    score = 0
    diff = 0.5**abs(np.diff(grid, axis=0))
    smaller_grid = np.minimum(grid[:-1], grid[1:])
    score += np.nansum(diff*smaller_grid)
    diff = 0.5**abs(np.diff(grid, axis=1))
    smaller_grid = np.minimum(grid[:,:-1], grid[:,1:])
    score += np.nansum(diff*smaller_grid) 
    return score 
def evaluate_lowerbound(board):
    if (not board.player_turn):
        return lowerbound_helper(board,[])
    max_val = board.score
    for move in PLAYER_MOVES:
        childboard = board.slide(move, True)
        if (childboard == board):
            continue
        h = lowerbound_helper(childboard,[move])
        #print (move, h)
        max_val = max(max_val, h)
    return max_val
def lowerbound_helper(board, valid_moves):
    if (board.is_empty):
        return board.score

    if (len(valid_moves)<2):  
        if (len(valid_moves)>0):
            lastmove = valid_moves[0]
            max_val = slide_helper(board, lastmove)
        else:
            lastmove = None
            max_val = board.score
        for move in PLAYER_MOVES:  
            if (move == INVALID_PLAYER_MOVES[lastmove]):
                continue         
            newboard = check_valid_board(board, move)
            if (newboard == board):
                continue
            if (move != lastmove):
                valid_moves.append(move)
            h = lowerbound_helper(newboard,valid_moves)
            #print (newboard, h)
            max_val = max(max_val, h)
            if (move != lastmove):
                valid_moves.remove(move)
    else:

        max_val = board.score
        for move in valid_moves:
            newboard = check_valid_board(board, move)
            if (newboard == board):
                continue
            h = lowerbound_helper(newboard,valid_moves)
            max_val = max(max_val, h)
    return max_val
def slide_helper(board, last_move):
    max_val = board.score
    #for move in valid_moves:
    childboard = board.slide(last_move, True)
    if (childboard == board):
        return max_val
    else:
        return slide_helper(childboard,last_move)
'''grid = board.grid_
if (move == "left"):
    newgrid = check_valid_grid(grid)
elif (move == "up"):
    newgrid = np.rot90(check_valid_grid(np.rot90(grid,1)),-1)
elif (move == "right"):
    newgrid = np.rot90(check_valid_grid(np.rot90(grid,2)),-2)
else:
    newgrid = np.rot90(check_valid_grid(np.rot90(grid,-1)),1)
newboard = Board2048(newgrid, True, board.score)
newboard = newboard.slide(move, True)'''
def check_valid_grid(grid):
    newgrid = grid.copy()
    for row in newgrid:
        for i in range(1, newgrid.shape[1]):
            row[i] = 0 if row[i-1]==0 else row[i]
    return newgrid
def move_line_helper(line,llen):
    score_added = 0
    newline = np.zeros(llen)
    i=0
    j=0
    while (j<line.shape[0]):
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
    return newline, score_added
def move_grid_helper(oldgrid):
    newgrid = []
    llen = oldgrid.shape[1]
    score_added = 0
    i=0
    for line in oldgrid:
        newline = np.zeros(llen)
        i=0
        while (i<llen):
            if (line[i]==0):
                i+=1
                continue
            for j in range(i, llen):
                if line[j] == 0 or j == llen-1:
                    jend = llen if j == llen-1 else j
                    newline_tmp, score_added_tmp = move_line_helper(line[i:jend], llen)     
                    score_added += score_added_tmp
                    if i==0:
                        newline = newline_tmp
                    i = j+1
                    break
        newgrid.append(newline)
    newgrid = np.array(newgrid)
    return newgrid, score_added

def check_valid_board(board, move):
    if (move == "left"):
        oldgrid = board.grid_
        newgrid, score_added = move_grid_helper(oldgrid)
    elif (move == "up"):
        oldgrid = np.rot90(board.grid_, 1)
        newgrid, score_added = move_grid_helper(oldgrid)
        newgrid = np.rot90(newgrid, -1)
    elif (move == "right"):
        oldgrid = np.rot90(board.grid_, 2)
        newgrid, score_added = move_grid_helper(oldgrid)
        newgrid = np.rot90(newgrid, 2)
    else:
        oldgrid = np.rot90(board.grid_, -1)
        newgrid, score_added = move_grid_helper(oldgrid)
        newgrid = np.rot90(newgrid, 1)
    
    return Board2048(newgrid, True, board.score+score_added)
def evaluate_score(board):
    #score for accumulated score
    cur_score = board.score#np.nansum(board.size**board.grid_)#
    cur_score = evaluate_lowerbound(board)#board.score#np.nansum(board.size**board.grid_)#

    #sum_score += 2*np.nansum(np.power(2**board.grid_,2)) 
    
    #score for edge and corner
    #esm_score += np.nansum( 2**board.grid_[0] + 2**board.grid_[board.size-1] + 2**board.grid_[:,0] + 2**board.grid_[:,board.size-1])
    #esm_score += np.sum(board.grid_[0] + board.grid_[board.size-1] + board.grid_[:,0] + board.grid_[:,board.size-1])
    
    
    #avg = np.nansum(board.grid_)/board.nonzero_counts
    #sum_score += board.zero_counts * 30 *avg
   
    #smoothness
    #smoothness += compute_smoothness(board.grid_)
    
    #print(board,"smooth penalty:",compute_smoothness(board.grid_))
    #monotonicity = compute_monotonicity(board.grid_)
    #print ("sum_score",sum_score)
    #if (board.player_turn):
    
        #print (board,cur_score-board.score)
    
    return cur_score #+ cnt_free * monotonicity

initial_grid = np.zeros((3,2))
initial_grid[0][0]=4
initial_grid[0][1]=8
initial_grid[1][0]=4
initial_grid[1][1]=64
initial_grid[2][1]=0
initial_board = Board2048(grid=initial_grid,player_turn=False,score=288)
h=evaluate_score(initial_board)
print (initial_board,h)