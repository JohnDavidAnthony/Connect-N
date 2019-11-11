from Visualization import Visualization, Board
from Game import Game
import random
import numpy as np
import pygame
import time

# 0: Empty, 1: Red, 2: Yellow

#Runs the game with Random piece placements
def main():
    width = 7
    height = 6
    back = Game(width, height)
    front = Visualization(600, 600)
    front.board = Board(width, height)

    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            exit()

        #Check for tie game
        if back.checkTie():
            print("Tie Game, No Winner")
            break

        #Blue makes a move and checks for win
        back.submitMove(random.randint(0, width - 1), 1)

        front.board.replace_board(np.rot90(np.array(back.grid), 3))
        front.update_screen()
        pygame.event.get()
        if back.checkWin(1):
            print("Red Wins!")
            break
        time.sleep(.25)


        #Red makes a move and checks for win
        back.submitMove(random.randint(0, width - 1), 2)
        front.board.replace_board(np.rot90(np.array(back.grid), 3))
        front.update_screen()
        pygame.event.get()
        if back.checkWin(2):
            print("Yellow Wins!")
            break

        time.sleep(.25)



    # back.submitMove(0, 1)
    # front.board.place_piece(0, 1)
    #
    # while True:
    #     front.update_screen()
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_LEFT]:
    #         exit()
    #     pygame.event.get()
    #

    #input()

    #while True:
    #     #Check for tie game
    #     if back.checkTie():
    #         print("Tie Game, No Winner")
    #         break
    #
    #     #Red makes a move and checks for win
    #     col = random.randint(0,3)
    #     back.submitMove(col, 1)
    #     front.board.place_piece(col, 1)
    #     if back.checkWin(1):
    #         print("Red Wins!")
    #         break
    #

    #     #Yellow makes a move and checks for win
    #     col = random.randint(0,3)
    #     back.submitMove(col, 2)
    #     front.board.place_piece(col, 2)
    #     if back.checkWin(2):
    #         print("Yellow Wins!")
    #         break
    #
    #     front.update_screen()
    #
    # back.printBoard()
    # print("Resetting Board")
    # back.resetBoard()

main()
