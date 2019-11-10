# LEGEND: B is Blue pieces, R is Red pieces, - is Empty spaces

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

    def submitMove(self, column, color):
        #Error checking move
        if column > (self.WIDTH - 1) or column < 0 :
            print("Column out of range.")
            return
        #Checking if column is full
        if self.grid[0][column] != '-':
            print("Column " + str(column) + " is full, cannot place piece here")
            return

        #Finding level to insert piece and changing the grid
        insertLevel = 0
        while insertLevel < self.HEIGHT:
            #Checking if bottom row is empty
            if insertLevel == self.HEIGHT - 1 and self.grid[insertLevel][column] == '-':
                self.grid[insertLevel][column] = color
                return
            #Checking if next row is full, if so place piece
            if self.grid[insertLevel + 1][column] != '-':
                self.grid[insertLevel][column] = color
                return
            #Increment insertLevel
            insertLevel += 1

    #TO-DO
    def checkWin(self):
        return

def main():
    b = Board(4, 4)

    print("Placing Blue piece at Column 0")
    b.submitMove(0, 'B')
    b.printBoard()

    print("Placing Red piece at Column 3")
    b.submitMove(3, 'R')
    b.printBoard()

    print("Placing Blue piece at Column 0")
    b.submitMove(0, 'B')
    b.printBoard()

    print("Resetting Board")
    b.resetBoard()
    b.printBoard()

main()
