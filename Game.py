# LEGEND - 0: Empty, 1: Red, 2: Yellow
import random

class Game:
    def __init__(self, width, height):
        # Feel free to Change to whatever board size we want
        self.WIDTH = width
        self.HEIGHT = height
        # Creates empty board
        self.grid = [[0 for y in range(self.WIDTH)] for x in range(self.HEIGHT)]

    #Prints board in easily readable format
    def printBoard(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == 1:
                    print(str(self.grid[y][x]) + " ", end = ''),
                elif self.grid[y][x] == 2:
                    print(str(self.grid[y][x]) + " ", end = ''),
                else:
                    print("-" + " ", end = ''),
            print()
        print()

    #Clears the board back to its original state
    def resetBoard(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                self.grid[y][x] = 0

    def getLegalMoves(self):
        legalMoves = []
        for i in range(0, len(self.grid[0])):
            if self.grid[0][i] == 0:
                legalMoves.append(i)
        return legalMoves

    def submitMove(self, column, colour):
        #Error checking move
        if column > (self.WIDTH - 1) or column < 0 :
            return
        #Checking if column is full
        if self.grid[0][column] != 0:
            return

        #Finding level to insert piece and changing the grid
        insertLevel = 0
        while insertLevel < self.HEIGHT:
            #Checking if bottom row is empty
            if insertLevel == self.HEIGHT - 1 and self.grid[insertLevel][column] == 0:
                self.grid[insertLevel][column] = colour
                return
            #Checking if next row is full, if so place piece
            if self.grid[insertLevel + 1][column] != 0:
                self.grid[insertLevel][column] = colour
                return
            #Increment insertLevel
            insertLevel += 1

    #THIS IS HARD CODED FOR CONNECT 4
    def checkWin(self, colour):
        # Check horizontal spaces
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH - 3):
                if self.grid[y][x] == colour and self.grid[y][x+1] == colour and self.grid[y][x+2] == colour and self.grid[y][x+3] == colour:
                    return True

        # Check vertical spaces
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT - 3):
                if self.grid[y][x] == colour and self.grid[y+1][x] == colour and self.grid[y+2][x] == colour and self.grid[y+3][x] == colour:
                    return True

        # Check / diagonal spaces
        for x in range(self.WIDTH - 3):
            for y in range(2, self.HEIGHT):
                if self.grid[y][x] == colour and self.grid[y-1][x+1] == colour and self.grid[y-2][x+2] == colour and self.grid[y-3][x+3] == colour:
                    return True

        # Check \ diagonal spaces
        for x in range(self.WIDTH - 3):
            for y in range(self.HEIGHT - 3):
                if self.grid[y][x] == colour and self.grid[y+1][x+1] == colour and self.grid[y+2][x+2] == colour and self.grid[y+3][x+3] == colour:
                    return True

        return False

    def checkTie(self):
        for x in range(0, len(self.grid[0])):
            if self.grid[0][x] == 0:
                return False
        return True
