import numpy as np
from GLOBAL import PLAYER_MOVES, METHODS,GAME_MOVES,PLAYER_NEXT_MOVE
from GLOBAL import LOWERBOUND,UPPERBOUD,EXACT
import math
from itdeepening_timer import TimeOut
from static_evaluation import evaluate_score
from initial_states import InitialStates, generate2by2,generate3by2
from board import Board2048
import time
import csv
import pickle

cnt_nodes = 0
cnt_nodes_it = 0 
is_complete = True
def minimax_alphabeta_moves(board, depth_limit=10000, node_ordering=True):
    #print(board, board.player_turn)
    global cnt_nodes,cnt_nodes_it, is_complete
    cnt_nodes=0
    cnt_nodes_it=0
    trans_table = {}
    best_val,d,best_move,end_board = minimax_alphabeta(board, depth_limit, depth_limit, -math.inf, math.inf, trans_table, {},{}, node_ordering)
     
    print ("Return the result of depth {}: selected move {} with value {}".format(d, best_move, best_val)) 
    print ("depth:{}, total nodes:{}, current nodes:{}. value:{}, move:{}, d:{}, size of table:{}".format(depth_limit,cnt_nodes,cnt_nodes_it,best_val,best_move,d,len(trans_table)))
    print ("end state{}, is_complete{}".format(end_board,is_complete))
    #print (trans_table)
    return best_move
def minimax_alphabeta_itdeepening(board, timeout):
    depth_limit =  1# depth of the current search
    timeout = 100000
    old_table = {}
    trans_table = {}
    node_ordering = True
    global cnt_nodes, cnt_non_leaf_nodes, cnt_restore_nodes,cnt_nodes_it, is_complete
    cnt_nodes = 0
    start = time.time()
    try:
        TimeOut(timeout).start()
        while True:    
            cnt_nodes_it = 0
            is_complete = True
            trans_table={}
             
            best_val,d,best_move,is_end = minimax_alphabeta(board, depth_limit,depth_limit, -math.inf, math.inf, trans_table, old_table,{}, node_ordering)
            print ("depth {}: total nodes:{},Current nodes: {}  value:{}, move:{}, d:{}, size of table:{} time {}s is complete:{})".format(depth_limit,cnt_nodes,cnt_nodes_it,best_val,best_move,d,len(trans_table),time.time()-start, is_complete))
            old_table = trans_table
            if (is_complete):
                break
            depth_limit += 1
    except TimeOut.TimeOutException as e:
        print(e) # If we are not bothered by nanosecond differences, this is good enough
    #best_move = moves_seq
    print ("Return the result of depth {}: selected move {} with value {}".format(depth_limit-1, best_move, best_val))    
    return best_move
#generate ordered nodes
def order_moves(child_boards_moves, max_node, old_table):
    score_dict={}
    idx = 0
    for (child_board, _) in child_boards_moves:
        if (child_board  in old_table):
            val,_,_, flag = old_table[child_board]#
            if (flag == UPPERBOUD):
                val = evaluate_score(child_board)####
        else:
            val = evaluate_score(child_board)#### 

        score_dict[idx] = val
        idx+=1
        #if (len(set(score_dict.values()))>1):
        #    print ([child_boards_moves[idx][1] for idx in score_dict])
    ordered_child_boards=[]
    
    for key in sorted(score_dict, key=score_dict.__getitem__, reverse=max_node):
        ordered_child_boards.append(child_boards_moves[key])
    if (set(ordered_child_boards)!=set(child_boards_moves)):
        print ("error")
    #print("after sorted",score_dict)
    return ordered_child_boards

##minimax search with alpha beta pruning
def minimax_alphabeta(board, depth_limit, depth, alpha, beta, trans_table, old_table, heuristic_table, node_ordering):
    global cnt_nodes, cnt_nodes_it,initial_board,is_complete

    cnt_nodes+=1  
    cnt_nodes_it+=1
    alphaOrig = alpha
    """transposition_table"""
    for b in board.generate_sym():
        if b in trans_table:
            val, d, end_board,  flag = trans_table[b]
            if (d >= depth):#(d + depth >= depth_limit )#larger to the current search depth 
                if (flag == EXACT):  
                    return (val+board.score, d, end_board)# , i_move)
                elif (flag == UPPERBOUD):   #must be MIN node
                    beta = min(beta, val+board.score)
                else:
                    alpha = max(alpha, val+board.score)
            ###???????? is the lower bound of the minimax always the lower bound
            #elif ( (flag == EXACT or flag == LOWERBOUND)): #we only use it as the lower bound
            #    alpha = max(alpha, val+board.score)  
            if (alpha>=beta):  
                return (val+board.score, d, end_board)#, i_move)
            board = b
            break
         
    ######shall take a max? No, hval won't be smaller than val which is old beta or old alpha
    ###??? shall I record it? No need
    ####??? shall I update the alpha
    #trans_table[board] = (hval-board.score, 0, board.end_board,  EXACT)
    if (board in heuristic_table):
        hval = heuristic_table[board] + board.score
    else:
        hval = evaluate_score(board) 
        heuristic_table[board]=hval - board.score
    #hval = evaluate_score(board)
    alpha = max(alpha, hval) 
    if (hval>=beta):  
        """pruning for lower bound of the heuristic""" 
        if (not board.player_turn):
            print ("Strange!!!",board,hval, alphaOrig)
        return hval,depth,None
    #hval = board.score#evaluate_score(board) 
    if ((depth <= 0 ) or board.is_ended) :
        #trans_table[board] = (hval-board.score, depth, board.end_board,  EXACT)
        if (not board.is_ended):
            is_complete = False
        """static value"""
        return hval,depth,board
    
    child_boards_moves=[]
    best_move = None
    end_board = None
    # max node
    if board.player_turn:
        best_val= -math.inf
        for move in PLAYER_MOVES:
            child_board = board.slide(move)
            if child_board.is_same(board):
                continue
            child_boards_moves.append((child_board, move))
        if node_ordering:
            child_boards_moves = order_moves(child_boards_moves,  True, old_table)
        
        for (child_board, move) in child_boards_moves:
            hvalue, tempd, ie =  minimax_alphabeta(child_board, depth_limit, depth-1, alpha, beta, trans_table, old_table, heuristic_table, node_ordering)
            if (hvalue > best_val):
                best_val = hvalue
                best_move = move
                end_board = ie #and end_board
            alpha = max(alpha, best_val)
            if beta <= alpha:
                break
    else:
        best_val= math.inf
        for move in GAME_MOVES(board):
            child_board = board.place((move[0], move[1]), move[2])
            child_boards_moves.append((child_board, move))
        
        if node_ordering:
            child_boards_moves = order_moves(child_boards_moves, False, old_table)
        
        for (child_board, move) in child_boards_moves:
            hvalue,tempd,ie =  minimax_alphabeta(child_board, depth_limit, depth-1, alpha, beta, trans_table, old_table, heuristic_table, node_ordering)
         
            if (hvalue < best_val):
                best_val = hvalue
                best_move = move
                end_board = ie
            #end_board = ie and end_board
            beta = min(beta, best_val)
            if beta <= alpha:
                break
    """update transposition table"""
    if (best_val <= alphaOrig):#alphaOrig
        trans_table[board]=(best_val-board.score, depth, end_board, UPPERBOUD)
    elif (best_val >= beta):
        trans_table[board]=(best_val-board.score, depth, end_board, LOWERBOUND)
    else:
        trans_table[board]=(best_val-board.score, depth, end_board,  EXACT)

    if (depth_limit == depth):
        return (best_val,depth,best_move,end_board)
    else:
        return (best_val,depth,end_board)

if __name__ == "__main__":
    choice = int(input("Please specify the size of the game: 1:2*2, 2:2*3, 3:3*2, 4:3*3, 5:3*4, 6:4*3, 7:4*4\n"))
    choice_dict = {1:(2,2), 2:(2,3), 3:(3,2), 4:(3,3), 5:(3,4), 6:(4,3), 7:(4,4)}
    shape = choice_dict[int(choice)]
    if (choice == 1):
        initial_grid_list = generate2by2()
    elif (choice == 3):
        initial_grid_list = generate3by2()
    csvfile = open("log_size{0}*{1}_24.csv".format(shape[0],shape[1]), "w")
    writer = csv.writer(csvfile)
    writer.writerow(['initial state','end state','score','max value','time(s)', 'number of nodes'])
    i = 0
    for initial_grid in initial_grid_list:#[58:59]: #58 True 10 false
        i+=1
        print ("############################################ New Game ##################################################",i)  
        cnt_nodes = 0
        cnt_nodes_it = 0
        is_complete = True

        board = Board2048(grid=initial_grid,player_turn=True,score=0)
        print ("initial board:", board)
        depth_limit = 50000
        trans_table = {}
        try:
            with open('{0}*{1}_data.pkl'.format(shape[0],shape[1]),'rb') as data_file:    
                heuristic_table = pickle.load(data_file)
                print (len(heuristic_table))
        except:
            heuristic_table = {}
        #heuristic_table = {}
        start = time.time()

        best_val,d,best_move,end_board = minimax_alphabeta(board, depth_limit, depth_limit, -math.inf, math.inf, trans_table, {}, heuristic_table, node_ordering=True)
        
        with open('{0}*{1}_data.pkl'.format(shape[0],shape[1]), 'wb') as outfile:
            pickle.dump(heuristic_table, outfile)
        print ("Return the result of depth {}: selected move {} with value {}".format(d, best_move, best_val)) 
        print ("depth:{}, total nodes:{}, current nodes:{}. value:{}, move:{}, d:{}, size of t table:{},h table{}".format(depth_limit,cnt_nodes,cnt_nodes_it,best_val,best_move,d,len(trans_table), len(heuristic_table)))
        print ("end state{}, is_complete:{}".format(end_board, is_complete))
       
        #end_board, steps = Game2048(initial_grid, "ai","ai",method_idx=2).play()
        writer.writerow([board, end_board, best_val, 16,  time.time()-start, cnt_nodes])


##brute force minimax search
'''def minimax_search(board, depth):
    if (depth <= 0 or board.end_board):
        """static value"""
        return evaluate_score(board) 
    else:
        if board.player_turn:
            best_val= -math.inf
            for move in PLAYER_MOVES:
                child_board = board.slide(move)
                if child_board == board:
                    continue
                best_val= max(best_val, minimax_search(child_board, depth-1))
            return best_val
        else:
            best_val= math.inf
            for move in GAME_MOVES(board):
                child_board = board.place((move[0], move[1]), move[2])
                best_val= min(best_val, minimax_search(child_board, depth-1))
            #print("hvalue for computer", best_val)
            return best_val'''