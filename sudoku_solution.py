

import pyautogui, time


class SudokuSolution:

    def __init__(self):
        pass


    def sudoku_mouse_solution(self, puzzle, solution, x,y,w,h):
    
        w_box = int(w / 9)
        h_box = int(h / 9)
        
        x_start = x + w_box / 2
        y_start = y + h_box / 2
        
        pyautogui.moveTo(x_start, y_start)
        pyautogui.click()
    
        for i in range(9):
            if i % 2 == 0:
                for j in range(9):
                    
                    if puzzle[i][j] == 0:
                        pyautogui.click()
                        pyautogui.typewrite(str(solution[i][j]))
                        
                    if j < 8:
                        pyautogui.moveRel(w_box, 0)
                    
            else:
                for j in range(8,-1,-1):
                
                    if puzzle[i][j] == 0:
                        pyautogui.click()
                        pyautogui.typewrite(str(solution[i][j]))
                        
                    if j > 0:
                        pyautogui.moveRel(-w_box, 0)		

            if i < 8:
                pyautogui.moveRel(0, h_box)
    

    def sudoku_arrow_solution(self, puzzle, solution, x,y,w,h):

        w_box = int(w / 9)
        h_box = int(h / 9)
        
        x_start = x + w_box / 2
        y_start = y + h_box / 2
        
        pyautogui.moveTo(x_start, y_start)
        pyautogui.click()
        
        for i in range(9):
            if i % 2 == 0:
                for j in range(9):
                
                    if puzzle[i][j] == 0:
                        pyautogui.typewrite(str(solution[i][j]))
                    
                    if j < 8:
                        pyautogui.press('right')
                    
            else:
                for j in range(8,-1,-1):
                
                    if puzzle[i][j] == 0:
                        pyautogui.typewrite(str(solution[i][j]))
                        
                    if j > 0:
                        pyautogui.press('left')			

            if i < 8:
                pyautogui.press('down')
                           