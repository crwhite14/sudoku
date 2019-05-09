
#USAGE
#python sudoku.py

'''
Given an online Sudoku game (e.g. sudoku.com, komoroske.com/sudoku)
this module will detect the Sudoku game, find the solution,
and automatically input the solution by typing the correct number
in each box
'''

import math
import copy
import numpy as np
import argparse

#local imports
from sudoku_detection import SudokuDetection
from sudoku_solution import SudokuSolution
from sudoku_solver import SudokuSolver

ap = argparse.ArgumentParser()
ap.add_argument("solution_method", help="mouse or arrow")
args = vars(ap.parse_args())

sd = SudokuDetection()
ss = SudokuSolution()
ss2 = SudokuSolver()

puzzle, x,y,w,h = sd.get_puzzle_from_screen()
p = copy.deepcopy(puzzle)
solution = ss2.solver(p)

print('input')
sd.print_sudoku(puzzle)
print('solution')
sd.print_sudoku(solution)

if args["solution_method"] == 'mouse':
    ss.sudoku_mouse_solution(puzzle, solution, x,y,w,h)
else:
    ss.sudoku_arrow_solution(puzzle, solution, x,y,w,h)


