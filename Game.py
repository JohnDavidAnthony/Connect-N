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
            print("Column out of range.")
            return
        #Checking if column is full
        if self.grid[0][column] != 0:
            print("Column " + str(column) + " is full, cannot place piece here")
            return
        #Error checking colours and printing out move
        if colour == 2:
            print("Inserting Yellow piece in column: " + str(column))
        elif colour == 1:
            print("Inserting Red piece in column: " + str(column))
        else:
            print("Incorrect Colour, cannot place")
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

    #THIS IS HARD CODED FOR CONNECT 3
    def checkWin(self, colour):
        # Check horizontal spaces
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH - 2):
                if self.grid[y][x] == colour and self.grid[y][x+1] == colour and self.grid[y][x+2] == colour:
                    return True

        # Check vertical spaces
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT - 2):
                if self.grid[y][x] == colour and self.grid[y+1][x] == colour and self.grid[y+2][x] == colour:
                    return True

        # Check / diagonal spaces
        for x in range(self.WIDTH - 2):
            for y in range(2, self.HEIGHT):
                if self.grid[y][x] == colour and self.grid[y-1][x+1] == colour and self.grid[y-2][x+2] == colour:
                    return True

        # Check \ diagonal spaces
        for x in range(self.WIDTH - 2):
            for y in range(self.HEIGHT - 2):
                if self.grid[y][x] == colour and self.grid[y+1][x+1] == colour and self.grid[y+2][x+2] == colour:
                    return True

        return False

    def checkTie(self):
        for x in range(0, len(self.grid[0])):
            if self.grid[0][x] == 0:
                return False
        return True

#Runs the game with Random piece placements
# def main():
#     Width = 10
#     Height = 15
#     b = Game(10, 15)
#     while True:
#         #Check for tie game
#         if b.checkTie():
#             print("Tie Game, No Winner")
#             break
#
#         #Blue makes a move and checks for win
#         b.submitMove(random.randint(0,Width - 1), 1)
#         if b.checkWin(1):
#             print("Red Wins!")
#             break
#
#         #Red makes a move and checks for win
#         b.submitMove(random.randint(0,Width - 1), 2)
#         if b.checkWin(2):
#             print("Yellow Wins!")
#             break
#
#     b.printBoard()
#     print("Resetting Board")
#     b.resetBoard()
#
# main()
