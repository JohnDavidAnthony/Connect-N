import numpy as np
import pygame


# Class that controls drawing things to the screen
class Visualization:
    def __init__(self, screen_width, screen_height):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        clock.tick(60)
        pygame.display.update()
        self.width = screen_width
        self.height = screen_height
        self.board = Board(0, 0)  # Temporary Board

    def update_board(self, board_arr):
        """
        Updates the game board
        :param board_arr: An array containing the location of the player pieces
        """
        self.board.square_width = self.width / len(board_arr)
        self.board.board_arr = board_arr

    def update_screen(self):
        """
        Prepares and then draws all components to screen
        """
        # Draw the piece under the mouse
        x, y = pygame.mouse.get_pos()
        left_click, _, _ = pygame.mouse.get_pressed()
        self.board.draw_mouse_piece(self.screen, self.width, x, left_click)

        # Draw the current state of the board
        self.board.draw_full_board(self.screen, self.width, self.height)

        pygame.display.update()


# Class that holds all the information needed to draw the board to the screen
class Board:
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    def __init__(self, num_cols, num_rows):
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.board_arr = np.zeros((num_cols, num_rows))
        self.current_player = 1
        self.clicked_last_frame = False

    def place_piece(self, col, player):
        """
        Updates the game board with the newly placed game piece
        :param col: The column to place the new piece
        :param player: The player number of the placed piece
        """
        for i in range(len(self.board_arr[col])):
            if self.board_arr[col][i] == 0:
                self.board_arr[col][i] = player
                break

    def replace_board(self, new_board):
        """
        Completely replaces the existing game board with a new board
        :param new_board: The new game board array
        """
        self.board_arr = new_board

    def draw_mouse_piece(self, screen, width, x, left_click):
        """
        Draws the game piece indicating what column to place the piece in on mouse click
        :param screen: The screen to add the piece too
        :param width: The width of the game screen
        :param x: The x position of the mouse
        :param left_click: Boolean indicating if mouse was pressed that frame
        """
        if self.current_player == 1:
            piece_colour = self.RED
        else:
            piece_colour = self.YELLOW

        square_width = int(width / len(self.board_arr))
        pygame.draw.rect(screen, self.BLACK, (0, 0, width, square_width))
        pygame.draw.circle(screen, piece_colour, (x, int(square_width / 2)), int(square_width / 2 - 5))

        if left_click:
            for i in range(self.num_cols):
                if (i + 1) * square_width > x >= i * square_width:
                    self.place_piece(i, self.current_player)
                    break

            # Set current player alternate between 1 and 2
            if self.current_player == 1:
                self.current_player = 2
            else:
                self.current_player = 1

    def draw_full_board(self, screen, width, height):
        """
        Used to draw the full game board,
        :param screen: The screen to draw the board too
        :param width: Width of screen
        :param height: Height of screen
        """
        square_width = int(width / len(self.board_arr))
        pygame.draw.rect(screen, self.BLUE, (0, square_width, width, height - square_width))

        current_y = int(height - square_width / 2)
        for row_index in range(len(self.board_arr[0])):
            current_x = int(square_width / 2)
            for col_index in range(len(self.board_arr)):

                cell = self.board_arr[col_index][row_index]
                piece_colour = self.BLACK
                if cell == 1:
                    piece_colour = self.RED
                elif cell == 2:
                    piece_colour = self.YELLOW

                pygame.draw.circle(screen, piece_colour, (current_x, current_y), int(square_width / 2 - 5))

                current_x += square_width
            current_y -= square_width


v = Visualization(1000, 1000)
v.board = Board(7, 6)

while True:
    v.update_screen()
    pygame.event.get()
