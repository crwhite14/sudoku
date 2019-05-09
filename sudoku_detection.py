
import argparse
from imutils import contours
import imutils
import cv2
import itertools
import numpy as np
import pyautogui, time

class SudokuDetection:

    def __init__(self):
    
        #set up reference font for the numbers. 
        #For some fonts, it might be necessary to change this reference
        ref = cv2.imread("pictures/reference_smartgames.jpg")
        ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
        ref = cv2.threshold(ref, 180, 255, cv2.THRESH_BINARY)[1]
        ref = cv2.bitwise_not(ref)
        
        ref_cnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ref_cnts = imutils.grab_contours(ref_cnts)
        ref_cnts = contours.sort_contours(ref_cnts, method='left-to-right')[0]
        
        self.digits = {}
        for i,c in enumerate(ref_cnts):
            x,y,w,h = cv2.boundingRect(c)
            roi = ref[y:y+h, x:x+w]
            roi_resized = cv2.resize(roi,(57,88))
            self.digits[i] = roi_resized
            
    def get_puzzle_from_screen(self):
    
        screen = pyautogui.screenshot()
        screen_array = np.array(screen) 
        screen = screen_array[:, :, ::-1].copy()
        
        # pre-process the image by resizing it, converting it to
        # graycale, blurring it, and computing an edge map		
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 50, 200, 255)		
        
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        displayCnt = None
        x,y,w,h = 0,0,0,0
 
        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            x,y,w,h = cv2.boundingRect(c)
            
            #assume the puzzle is the largest square
            if .9 * w < h < 1.1 * w:
                displayCnt = approx
                break

        pad_h = int(h / 9 / 30) 
        pad_w = int(h / 9/ 30)
        puzzle = None        
        puzzle = screen[y:y+h-pad_h, x+pad_w:x+w]
        
        return (self.process_puzzle(puzzle), x,y,w,h)
        
        

    def get_puzzle_from_file(self, file):

        image = cv2.imread(file)
        return self.process_puzzle(image)
        
    def process_puzzle(self, image):
        
        puzzle = [[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0]]

        height, width = image.shape[:2]
        box_height = int(height / 9.0)
        box_width = int(width / 9.0)
        trim_height = int(box_height / 7)
        trim_width = int(box_width / 7)
    
        for i in range(9):		
            for j in range(9):                        
                box = image[box_width*i+trim_width:box_width*(i+1)-trim_width,box_height*j+\
                    trim_height:box_height*(j+1)-trim_height].copy()
                puzzle[i][j] = self.get_digit(box)

        return puzzle


    def get_digit(self, image):

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.threshold(image, 180, 255, cv2.THRESH_BINARY)[1]
        image = cv2.bitwise_not(image)
        
        cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            cnts = contours.sort_contours(cnts, method='left-to-right')[0]
        
        d = 0
        for i,c in enumerate(cnts):
            x,y,w,h = cv2.boundingRect(c)
            
            digit = image[y:y+h, x:x+w]
            digit_resized = cv2.resize(digit,(57,88))
            
            scores = []
            
            #find the digit with the closest match
            for (digit, digitROI) in self.digits.items():
                result = cv2.matchTemplate(digit_resized, digitROI, cv2.TM_CCOEFF)
                (_,score,_,_) = cv2.minMaxLoc(result)
                scores.append(score)
            d = np.argmax(scores) + 1

        return d
                
    def print_sudoku(self, puzzle):
        for i in range(9):
            print(puzzle[i])