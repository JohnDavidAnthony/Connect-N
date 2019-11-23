from Visualization import *
from Game import *
import time
from keras.models import load_model, model_from_json


def get_computer_move(model, back):
    board_arr = back.grid
    # Flatten Board
    board_arr = np.array(board_arr)  # convert the grid to a numpy array - easier for machine learning
    board_arr = board_arr.flatten()  # first state from the board is an empty board

    all_actions = list(range(0, back.WIDTH))

    # get values of each action
    action_arr = model.predict(np.expand_dims(board_arr, 0), batch_size=1)
    action_arr = action_arr[0]

    # convert to lists to 2-tuple and sort by action value
    action_tuples = list(zip(all_actions, action_arr))
    action_tuples.sort(key=lambda x: x[1], reverse=True)

    # Check to see if action is a legal action, if not do next best action
    # legal moves
    legal_moves = back.getLegalMoves()
    for tuple in action_tuples:
        if tuple[0] in legal_moves:
            return tuple[0]

    return 0


# Resets Gameboard for front and backend
def resetGame(back, front):
    back.resetBoard()
    front.board.replace_board(np.rot90(np.array(back.grid), 3))
    front.board.current_player = random.randint(1, 2)


# Plays move for front and backend
def playMove(player, col):
    backEnd.submitMove(col, player)


if __name__ == "__main__":
    width = 7
    height = 6
    backEnd = Game(width, height)
    frontEnd = Visualization(500, 500)
    frontEnd.board = Board(width, height)
    frontEnd.board.current_player = random.randint(1, 2)

    # Load in model
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")

    # Computer == turn 1

    while True:
        # Press Left Arrow Key to exit game
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            exit()

        if frontEnd.board.current_player == 1:
            # Computer makes a move
            time.sleep(.7)
            # column_to_place = random.choice(backEnd.getLegalMoves())

            # Get computer Move
            column_to_place = get_computer_move(loaded_model, backEnd)

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
