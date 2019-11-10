# LEGEND: B is Blue pieces, R is Red pieces, - is Empty spaces
import random

class Board:
    def __init__(self, width, height):
        # Feel free to Change to whatever board size we want
        self.WIDTH = width
        self.HEIGHT = height
        # Creates empty board
        self.grid = [['-' for y in range(self.WIDTH)] for x in range(self.HEIGHT)]

    #Prints board in easily readable format
    def printBoard(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                print(self.grid[y][x] + " ", end = ''),
            print()
        print()

    #Clears the board back to its original state
    def resetBoard(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                self.grid[y][x] = '-'

    def submitMove(self, column, colour):
        #Error checking move
        if column > (self.WIDTH - 1) or column < 0 :
            print("Column out of range.")
            return
        #Checking if column is full
        if self.grid[0][column] != '-':
            print("Column " + str(column) + " is full, cannot place piece here")
            return
        #Error checking colours and printing out move
        if colour == "B":
            print("Inserting Blue piece in column: " + str(column))
        elif colour == "R":
            print("Inserting Red piece in column: " + str(column))
        else:
            print("Incorrect Colour, cannot place")
            return

        #Finding level to insert piece and changing the grid
        insertLevel = 0
        while insertLevel < self.HEIGHT:
            #Checking if bottom row is empty
            if insertLevel == self.HEIGHT - 1 and self.grid[insertLevel][column] == '-':
                self.grid[insertLevel][column] = colour
                return
            #Checking if next row is full, if so place piece
            if self.grid[insertLevel + 1][column] != '-':
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
            for y in range(3, self.HEIGHT):
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
            if self.grid[0][x] == '-':
                return False
        return True

#Runs the game with Random piece placements
def main():
    b = Board(4, 4)
    while True:
        #Check for tie game
        if b.checkTie():
            print("Tie Game, No Winner")
            break

        #Blue makes a move and checks for win
        b.submitMove(random.randint(0,3), "B")
        if b.checkWin("B"):
            print("Blue Wins!")
            break

        #Red makes a move and checks for win
        b.submitMove(random.randint(0,3), "R")
        if b.checkWin("R"):
            print("Red Wins!")
            break

    b.printBoard()
    print("Resetting Board")
    b.resetBoard()

main()
