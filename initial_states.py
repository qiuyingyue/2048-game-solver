import numpy as np
class InitialStates:
    size = 0
    def __init__(self, shape):
        self.shape = shape

    def generate(self, max_cnt=10000):

        shape = self.shape
        empty_grid = np.zeros(shape)
        #empty_grid.fill(np.nan)
        possible_values = [[2,2],[2,4],[4,4]]
        possible_places = [(i,j) for i in range(shape[0]) for j in range(shape[1])]
        grid_list = []
        cnt=0
        for i in range(len(possible_places)):
            for j in range(i+1, len(possible_places)):
                if possible_places[j][1] < possible_places[i][1]  :
                    continue
                for v in possible_values:
                    grid = empty_grid.copy()
                    place = possible_places[i]
                    grid[place[0]][place[1]] = v[0]
                    place = possible_places[j]
                    grid[place[0]][place[1]] = v[1]
                    grid_list.append(grid)
                    cnt+=1
                    print (cnt, grid)
                    
                    if (cnt >= max_cnt):
                        return grid_list
        
        return grid_list
            
def generate2by2():
    grid_list = []
    p_values = [[2,2],[2,4],[4,4]]
    p_places = [((0,0),(0,1)),((0,0),(1,1))]    
    cnt=0
    for pos in p_places:
        x1,y1 = pos[0]
        x2,y2 = pos[1]
        for v in p_values:
            grid = np.zeros((2,2))
            grid[x1][y1] = v[0]
            grid[x2][y2] = v[1]
            grid_list.append(grid.copy())
            #print (cnt, grid)
            cnt+=1
    return grid_list 
def generate3by2():
    grid_list = []
    p_values = [[2,2],[2,4],[4,4]]
    p_places = [((0,0),(0,1)),((0,0),(1,1)),((0,0),(1,0)),((1,0),(1,1)),((1,0),(2,1)),((1,0),(2,0)),((0,0),(2,1)),((0,0),(2,0))]    
    cnt=0
    for pos in p_places:
        x1,y1 = pos[0]
        x2,y2 = pos[1]
        for v in p_values:
            grid = np.zeros((3,2))
            grid[x1][y1] = v[0]
            grid[x2][y2] = v[1]
            grid_list.append(grid.copy())
            #print (cnt, grid)
            cnt+=1
    return grid_list   
#generate3by2()     

            
