from Board import Board
import pygame
from Pieces.Queen import Queen
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop


class Chess:
    size = 640
    tenth = 640 / 10
    board = Board(size)
    board.initialize_standard_board()
    pygame.display.flip()

    def game(self):
        done = True
        promotion = False
        new_game_screen = False
        selection = []
        while done is True:
            pygame.display.flip()
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = False  # exit while loop

                if event.type == pygame.MOUSEBUTTONDOWN and new_game_screen:
                    if pygame.mouse.get_pressed()[0]:  # left mouse button pressed
                        pos = pygame.mouse.get_pos()
                        x = self.tenth

                        # yes - new game box
                        if 3 * x <= pos[0] <= 4.5 * x: #and 7 * x <= pos[1] <= 8 * x:
                            self.board.clear_board()
                            self.board.initialize_standard_board()
                            pygame.display.flip()
                            self.board.white_turn = True  # if white won, it should be their turn again
                            self.game()  # make a new game

                        # no - new game box
                        if 5.5 * x <= pos[0] <= 7 * x and 7 * x <= pos[1] <= 8 * x:
                            done = False  # exit while loop

                if event.type == pygame.MOUSEBUTTONDOWN and promotion:  # promotion dialogue
                    if pygame.mouse.get_pressed()[0]:  # left mouse button pressed
                        pos = pygame.mouse.get_pos()

                        # Each box for each piece selection, if they don't press on the box, try again
                        x = self.tenth
                        if 1.5 * x <= pos[0] < 2.5 * x and 1.5 * x <= pos[1] <= 2.5 * x:
                            knight = Knight(color)
                            self.board.place_piece(square, knight)
                            self.board.deselect_board()
                            pygame.display.flip()
                            promotion = False
                        elif 3.5 * x <= pos[0] < 4.5 * x and 1.5 * x <= pos[1] <= 2.5 * x:
                            bishop = Bishop(color)
                            self.board.place_piece(square, bishop)
                            self.board.deselect_board()
                            pygame.display.flip()
                            promotion = False
                        elif 5.5 * x <= pos[0] < 6.5 * x and 1.5 * x <= pos[1] <= 2.5 * x:
                            rook = Rook(color)
                            self.board.place_piece(square, rook)
                            self.board.deselect_board()
                            pygame.display.flip()
                            promotion = False
                        elif 7.5 * x <= pos[0] < 8.5 * x and 1.5 * x <= pos[1] <= 2.5 * x:
                            queen = Queen(color)
                            self.board.place_piece(square, queen)
                            self.board.deselect_board()
                            pygame.display.flip()
                            promotion = False

                if event.type == pygame.MOUSEBUTTONDOWN:  # normal move
                    if pygame.mouse.get_pressed()[0]:  # left mouse button pressed
                        pos = pygame.mouse.get_pos()
                        square = self.board.get_square(pos)
                        selection.append(square)
                        self.board.select_piece(square)
                        pygame.display.flip()

            if len(selection) == 2:
                output = self.board.player_move(selection[0], selection[1])
                selection = []
                if output[0] == "Promotion":
                    color = output[1]
                    square = output[2]
                    pygame.display.flip()
                    promotion = True
                if output == "New_Game":
                    self.board.new_game_message()
                    pygame.display.flip()
                    new_game_screen = True

        self.board.print_move_list()


