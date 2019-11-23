from Visualization import *
from Game import *
import time


def get_computer_move():
    pass

#Resets Gameboard for front and backend
def resetGame(back, front):
    back.resetBoard()
    front.board.replace_board(np.rot90(np.array(back.grid), 3))
    front.board.current_player = random.randint(1,2)

#Plays move for front and backend
def playMove(player, col):
    backEnd.submitMove(col, player)




if __name__ == "__main__":
    width = 7
    height = 6
    backEnd = Game(width, height)
    frontEnd = Visualization(500, 500)
    frontEnd.board = Board(width, height)
    frontEnd.board.current_player = random.randint(1,2)

    # Computer == turn 1

    while True:
            #Press Left Arrow Key to exit game
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                exit()

            if frontEnd.board.current_player == 1:
                #Computer makes a move
                time.sleep(.7)
                column_to_place = random.choice(backEnd.getLegalMoves())
                playMove(1, column_to_place)
                frontEnd.board.current_player = 2
                frontEnd.board.place_piece(column_to_place, 1)
                frontEnd.update_screen()

            # User's turn
            elif frontEnd.board.current_player == 2:
                frontEnd.board.user_can_place = True
                while frontEnd.board.current_player == 2:
                    frontEnd.update_screen()
                    if frontEnd.mouse_placed_at is not None:
                        playMove(2, frontEnd.mouse_placed_at)
                        frontEnd.update_screen()
                        frontEnd.board.current_player = 1


            if backEnd.checkTie():
                print("Tie Game, No Winner")
                frontEnd.update_screen()
                time.sleep(2)
                resetGame(backEnd, frontEnd)

            elif backEnd.checkWin(1):
                print("Red Wins!")
                frontEnd.update_screen()
                time.sleep(2)
                resetGame(backEnd, frontEnd)

            elif backEnd.checkWin(2):
                print("Yellow Wins!")
                frontEnd.update_screen()
                time.sleep(2)
                resetGame(backEnd, frontEnd)


