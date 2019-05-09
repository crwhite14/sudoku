

import math
import copy
import numpy as np
from sudoku_detection import SudokuDetection
from sudoku_solution import SudokuSolution

class SudokuSolver:

    def __init__(self):
        pass

    def solver(self, puzzle):

        poss = [[[],[],[],[],[],[],[],[],[]],
                [[],[],[],[],[],[],[],[],[]],
                [[],[],[],[],[],[],[],[],[]],
                [[],[],[],[],[],[],[],[],[]],
                [[],[],[],[],[],[],[],[],[]],
                [[],[],[],[],[],[],[],[],[]],
                [[],[],[],[],[],[],[],[],[]],
                [[],[],[],[],[],[],[],[],[]],
                [[],[],[],[],[],[],[],[],[]]]			
                                
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    poss[i][j] = [1,2,3,4,5,6,7,8,9]
                    
        p, s, solved = self.logic_solver(puzzle, poss)

        if solved == True:
            return p
            
        else:
            solution = self.recur_solver(p, s)[0]
            return solution
                
    #recurs until the sudoku is solved
    def recur_solver(self, puzzle, poss):
            
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] == 0:
                    for k in poss[i][j]:
                        p = copy.deepcopy(puzzle)
                        s = copy.deepcopy(poss)
                        p[i][j] = k
                        s[i][j] = []
                        
                        p_logic, s_logic, solved = self.logic_solver(p, s)
                        failed = False
                        
                        if self.checker(p_logic) == False:
                            solved = False
                            failed = True
                            
                        if solved == True:
                            return [p_logic, s_logic, True]
                            
                        elif failed == False:						
                            [p_iter, s_iter, sol] = self.recur_solver(p_logic, s_logic)
                            if sol:
                                return [p_iter, s_iter, True]

                    return [[],[],False]
                            
    def logic_solver(self, puzzle, poss): 
        
        changed = True
        has_zero = True
        counter = 0

        while changed == True and has_zero == True:
            counter = counter + 1
            changed = False
            has_zero = False
            
            #for loop over all the positions, check if place is forced
            for i in range(9):		
                for j in range(9):
                    if puzzle[i][j] == 0:
                    
                        has_zero = True
                        if self.get_poss(puzzle, poss[i][j], [i,j])[1]:
                            changed = True

                            #update possible numbers for place [i][j]
                            poss[i][j] = self.get_poss(puzzle, poss[i][j], [i,j])[0] 
                        
                            if len(poss[i][j]) == 1:
                                puzzle[i][j] = poss[i][j].pop(0)
                            
            for i in range(0,9,1):
                for type in ["r","c","b"]:
                    update = self.num_check(puzzle, poss, type, i)
                    if update[1] != 0:
                        puzzle[update[0][0]][update[0][1]] = update[1]
                        poss[update[0][0]][update[0][1]] = []
                        changed = True
                        
        return [puzzle, poss, not has_zero]
                

    #Given number x, row/col/box, num of r/c/b, check if there's one place for it. 
    #return 1..9 if true, 0 if false
    def num_check(self, puzzle, poss, type, num): 

        inds = []	
        
        if type == "r":
            for i in range(0,9,1):
                inds.append([num,i])
        elif type == "c":
            for j in range(0,9,1):
                inds.append([j,num])
        else:
            index_1 = (num % 3) * 3
            index_2 = math.floor(num / 3) * 3		
        
            inds = [[index_1,index_2],[index_1,index_2+1],[index_1,index_2+2],
            [index_1+1,index_2],[index_1+1,index_2+1],[index_1+1,index_2+2],
            [index_1+2,index_2],[index_1+2,index_2+1],[index_1+2,index_2+2]]	
                
        total_poss = []
        for ind in inds:
            if puzzle[ind[0]][ind[1]] == 0:
                for i in poss[ind[0]][ind[1]]:
                    total_poss.append(i)
            else:
                total_poss.append(puzzle[ind[0]][ind[1]])
            
        for i in range(1,10,1):
            if total_poss.count(i) == 1:
                for ind in inds:
                    if puzzle[ind[0]][ind[1]] == 0:
                        if i in poss[ind[0]][ind[1]]:
                            return [ind,i]	
                            
        return [[0,0],0]	
        

    def checker(self, puzzle):
        
        failed = False
        
        for i in range(0,9,1):
            r = self.get_row(puzzle, [i,i])
            for k in range(1,10,1):
                if r.count(k) > 1:
                    failed = True
                    
        for i in range(0,9,1):
            c = self.get_col(puzzle, [i,i])
            for k in range(1,10,1):
                if c.count(k) > 1:
                    failed = True	

        for i in range(0,9,1):
        
            index_1 = (i % 3) * 3
            index_2 = math.floor(i / 3) * 3		
            b = self.get_box(puzzle, [index_1,index_2])
            for k in range(1,10,1):
                if c.count(k) > 1:
                    failed = True
        
        return not failed
                    

    def get_poss(self, puzzle, old_poss, position):
    
        blockers_dup = self.get_row(puzzle, position) \
            + self.get_col(puzzle, position) + self.get_box(puzzle, position)
        blockers = []
        for i in blockers_dup:
            if i not in blockers:
                blockers.append(i)
        if 0 in blockers:
            blockers.remove(0)
            
        new_poss = []
        changed = False
        for i in old_poss:
            if i in blockers:
                changed = True
            else:
                new_poss.append(i)
            
        return [new_poss,changed]
            
    def get_row(self, puzzle, position):
        return puzzle[position[0]][:]
        
    def get_col(self, puzzle, position):
        return [row[position[1]] for row in puzzle]
        
    def get_box(self, puzzle, position):
        index_1 = math.floor(position[0] / 3) * 3
        index_2 = math.floor(position[1] / 3) * 3	
        to_return = puzzle[index_1][index_2:index_2+3] + puzzle[index_1+1][index_2:index_2+3] \
            + puzzle[index_1+2][index_2:index_2+3]
        
        return to_return
        
    def print_sudoku(self, puzzle):
        for i in range(0,9,1):
            print(puzzle[i])
