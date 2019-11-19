from Visualization import Visualization, Board
from Game import Game
import random
import numpy as np
import pygame
import time

# 0: Empty, 1: Red, 2: Yellow

#Plays move for front and backend
def playMove(player, col):
    back.submitMove(random.randint(0, width - 1), player)
    front.board.replace_board(np.rot90(np.array(back.grid), 3))
    front.update_screen()
    pygame.event.get()

#Resets Gameboard for front and backend
def resetGame():
    back.resetBoard()
    front.board.replace_board(np.rot90(np.array(back.grid), 3))
    front.update_screen()
    pygame.event.get()

#Global Parameters
width = 7
height = 6
back = Game(width, height)
front = Visualization(600, 600)
front.board = Board(width, height)

#Runs the game with Random piece placements
def main():
    #Keeping Track of wins and games played
    gamesPlayed = 0
    redWins = 0
    yellowWins = 0
    turn = 1
    while gamesPlayed < 10:
        while True:
            #Press Left Arrow Key to exit game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                exit()

            #Check for tie game
            if back.checkTie():
                print("Tie Game, No Winner")
                gamesPlayed += 1
                resetGame()
                break

            if turn == 1:
                #Blue makes a move and checks for win
                playMove(1, random.choice(back.getLegalMoves()))
                if back.checkWin(1):
                    print("Red Wins!")
                    gamesPlayed += 1
                    redWins += 1
                    resetGame()
                    break
                time.sleep(.1)

                #Red makes a move and checks for win
                playMove(2, random.choice(back.getLegalMoves()))
                if back.checkWin(2):
                    print("Yellow Wins!")
                    gamesPlayed += 1
                    yellowWins += 1
                    resetGame()
                    break
                time.sleep(.1)


            #Red goes first
            elif turn == 2:
                #Red makes a move and checks for win
                playMove(2, random.choice(back.getLegalMoves()))
                if back.checkWin(2):
                    print("Yellow Wins!")
                    gamesPlayed += 1
                    yellowWins += 1
                    resetGame()
                    break
                time.sleep(.1)

                #Blue makes a move and checks for win
                playMove(1, random.choice(back.getLegalMoves()))
                if back.checkWin(1):
                    print("Red Wins!")
                    gamesPlayed += 1
                    redWins += 1
                    resetGame()
                    break
                time.sleep(.1)

        if turn == 1:
            turn = 2
        else:
            turn = 1

    #Printing out results
    print("Red Wins: " + str(redWins))
    print("Yellow Wins: " + str(yellowWins))

main()
