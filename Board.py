import pygame
from PygameClient import PygameClient
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Pieces.King import King
from Pieces.Queen import Queen
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight


class Board(PygameClient):
    def __init__(self, size):
        super().__init__(size)

    # TURN BASED GAME-PLAY______________________________________________________________________________________________
    white_turn = True  # keep track of who's turn it is
    move_list = []  # keep track of all the moves during the game
    move_num = 0  # keep track of number of moves

    def player_move(self, square1, square2):
        if not self.legal_move(square1, square2):  # check that its a legal move
            self.deselect_board()
            return "", ""
        if self.white_turn:
            self.white_player_move(square1, square2)  # move the piece
            self.move_list.append((square1, square2))  # save the move as a tuple
            self.deselect_board()  # deselect 2 squares
            self.move_num += 1  # keep track of total game move
            self.update_white_attacks()  # update which squares white is attacking

            if self.checkmate(self.BLACK):  # CHECKMATE
                self.win_message(self.WHITE)
                return "New_Game"
            if self.stalemate(self.BLACK):  # STALEMATE
                self.stalemate_message()
                return "New_Game"
            if self.three_move_repetition():  # THREE MOVE REPETITION
                self.three_move_repetition_message()
                return "New_Game"
            if self.promotion(square2, self.WHITE):  # PROMOTION
                self.promotion_message(self.WHITE)
                return "Promotion", 1, square2

        else:
            self.black_player_move(square1, square2)
            self.move_list.append((square1, square2))
            self.deselect_board()
            self.move_num += 1
            self.update_black_attacks()

            if self.checkmate(self.WHITE):
                self.win_message(self.BLACK)
                return "New_Game"
            if self.stalemate(self.WHITE):
                self.stalemate_message()
                return "New_Game"
            if self.three_move_repetition():
                self.three_move_repetition_message()
                return "New_Game"
            if self.promotion(square2, self.BLACK):
                self.promotion_message(self.BLACK)
                return "Promotion", 0, square2
        return "", ""

    def white_player_move(self, square1, square2):
        # validate piece they want to move is white
        x1 = square1[0]
        y1 = square1[1]

        if self.square_taken(square1) and self.position[x1][y1].color == self.WHITE:  # if it is a white piece
            # move the piece
            if self.move_piece(square1, square2) is True:  # this will move the piece automatically
                self.white_turn = False  # todo in player_move method, it would still add this to the move list
            else:
                return

    def black_player_move(self, square1, square2):
        # validate piece they want to move is black
        x1 = square1[0]
        y1 = square1[1]

        if self.square_taken(square1) and self.position[x1][y1].color == self.BLACK:  # if it is a black piece
            # move the piece
            if self.move_piece(square1, square2) is True:
                self.white_turn = True
            else:
                return

    def print_move_list(self):
        for i in self.move_list:
            print(i)

    # BOARD PLAYER INPUT ______________________________________________________________________________________________
    # square is (0-7) coordinates
    # pos is xy pixel axis from pygame

    def get_square(self, pos):
        eighth = self.size / 8
        x = int(pos[0] // eighth)
        y = int(7 - (pos[1] // eighth))
        return x, y

    def get_pos(self, square):
        # returns top left pos of a square given its square coordinates
        x = square[0]
        y = 7 - square[1]

        x_pos = x * self.square_size
        y_pos = y * self.square_size

        return x_pos, y_pos

    # Board Drawing methods____________________________________________________________________________________________
    grid_color = [[0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0]]  # 0 is dark, 1 is white

    def draw_square(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))

    def select_piece(self, square):
        if not self.square_taken(square):
            return

        piece = self.get_piece(square)
        white_piece = piece.white_piece()

        if self.square_taken(square):  # checks that there is a piece there
            x_pos, y_pos = self.get_pos(square)
            piece = self.get_piece(square)

            # erase piece
            self.erase_piece(square)

            # recolor square (red if wrong piece for the player, gray if correct)
            if white_piece and self.white_turn:
                self.draw_square(x_pos, y_pos, self.LIGHT_GRAY)
            if not white_piece and self.white_turn:
                self.draw_square(x_pos, y_pos, self.LIGHT_RED)

            if white_piece and not self.white_turn:
                self.draw_square(x_pos, y_pos, self.LIGHT_RED)
            if not white_piece and not self.white_turn:
                self.draw_square(x_pos, y_pos, self.LIGHT_GRAY)

            # draw piece back on top
            self.draw_piece(square, piece)

    def color_square(self, square, color):
        x_pos, y_pos = self.get_pos(square)
        piece = self.get_piece(square)

        # erase piece
        self.erase_piece(square)

        # recolor square (red if wrong piece for the player, gray if correct)
        self.draw_square(x_pos, y_pos, color)

        # draw piece back on top (if there used to be a piece there)
        if self.square_taken(square):
            self.draw_piece(square, piece)

    def deselect_piece(self, square):
        if self.square_taken(square):
            x_pos, y_pos = self.get_pos(square)
            piece = self.get_piece(square)

            # erase piece
            self.erase_piece(square)

            # recolor square
            if self.is_white_square(square):
                self.draw_square(x_pos, y_pos, self.OFF_WHITE)
            else:
                self.draw_square(x_pos, y_pos, self.GREEN)

            # draw back on top
            self.draw_piece(square, piece)

    def deselect_board(self):
        self.screen.fill(self.background_color)
        self.draw_board()  # draw the board ^

        for i in range(0, 8):
            for j in range(0, 8):  # draw the pieces back on top
                square = i, j
                if self.square_taken(square):
                    self.deselect_piece(square)

    def is_white_square(self, square):
        x = square[0]
        y = square[1]
        if self.grid_color[x][y] == 1:
            return True

    def draw_white_row(self, y):
        for i in [1, 3, 5, 7]:
            self.draw_square(self.square_size * i, y, self.square_color)

    def draw_black_row(self, y):
        for i in [0, 2, 4, 6]:
            self.draw_square(self.square_size * i, y, self.square_color)

    def draw_board(self):
        for i in [0, 2, 4, 6]:
            self.draw_white_row(self.square_size * i)
        for i in [1, 3, 5, 7]:
            self.draw_black_row(self.square_size * i)

    def initialize_standard_board(self):
        self.draw_board()
        # create and place 32 pieces
        for i in range(0, 8):
            self.place_piece([i, 1], Pawn(1))
            self.place_piece([i, 6], Pawn(0))

        self.place_piece([0, 0], Rook(1))
        self.place_piece([7, 0], Rook(1))
        self.place_piece([0, 7], Rook(0))
        self.place_piece([7, 7], Rook(0))

        self.place_piece([4, 0], King(1))
        self.place_piece([4, 7], King(0))

        self.place_piece([3, 0], Queen(1))
        self.place_piece([3, 7], Queen(0))

        self.place_piece([2, 0], Bishop(1))
        self.place_piece([5, 0], Bishop(1))
        self.place_piece([2, 7], Bishop(0))
        self.place_piece([5, 7], Bishop(0))

        self.place_piece([1, 0], Knight(1))
        self.place_piece([6, 0], Knight(1))
        self.place_piece([1, 7], Knight(0))
        self.place_piece([6, 7], Knight(0))

    def draw_piece(self, coordinates, piece):
        x = coordinates[0]
        y = coordinates[1]
        x1, y1 = self.coordinates_to_pygame_axis([x, y])
        piece.draw(self.screen, x1, y1, self.square_size)

    def erase_piece(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        x1, y1 = self.coordinates_to_pygame_axis([x, y])

        if not self.is_white_square((x, y)):
            color = self.GREEN
        else:
            color = self.OFF_WHITE

        self.draw_square(x1, y1, color)

    def mark_white_attacks(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.white_attacks[i][j] == 1:
                    self.color_square((i, j), self.LIGHT_RED)

    def mark_black_attacks(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.black_attacks[i][j] == 1:
                    self.color_square((i, j), self.LIGHT_RED)

    def clear_board(self):
        self.position = [[None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None]]  # reset pieces

        self.screen.fill(self.background_color)  # re-draw board
        self.draw_board()  # draw the board ^

    # BACKEND Game Methods______________________________________________________________________________________________
    position = [[None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None]]

    white_attacks = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

    black_attacks = [[0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0]]

    white_castled = False
    black_castled = False

    def place_piece(self, square, piece):
        x = square[0]
        y = square[1]
        self.position[x][y] = piece
        self.erase_piece([x, y])  # if a piece captures another we erase the old piece
        self.draw_piece([x, y], piece)

    def get_piece(self, square):
        x = square[0]
        y = square[1]

        if self.position[x][y] is not None:  # check that it is not an 'EmptySquare' object
            return self.position[x][y]
        else:
            return None

    def remove_piece(self, square):
        x = square[0]
        y = square[1]
        self.position[x][y] = None
        self.erase_piece([x, y])

    def move_piece(self, square1, square2):
        """
        :param square1: [x, y]
        :param square2: [x2, y2]
        :param piece: Piece object
        :return: True if it was a legal move and was executed, false otherwise
        """
        piece = self.get_piece(square1)
        if self.square_taken(square2):
            piece2 = self.get_piece(square2)  # if there is a piece on the 2nd square save it
        else:
            piece2 = None
        white_piece = piece.white_piece()

        # CASTLE
        if not self.white_castled:
            if self.legal_castle(square1, square2, piece):  # if castling is legal, and white hasn't castled
                self.castle(square1, square2, piece)  # castle
                self.white_castled = True
                return True

        if not self.black_castled:
            if self.legal_castle(square1, square2, piece):
                self.castle(square1, square2, piece)  # castle
                self.black_castled = True
                return True

        # EN PASSANT
        if self.legal_en_passant(square1, square2, piece):
            self.en_passant(square1, square2, piece)
            return True

        # PIN
        if self.illegal_move_pin(square1, square2):
            return False

        # check if it is a legal move
        if self.legal_move(square1, square2):
            self.remove_piece(square1)
            self.place_piece(square2, piece)

            # if the king is still in check it is illegal. move the piece back and return false
            self.update_white_attacks()
            self.update_black_attacks()
            if white_piece and self.king_in_check(self.WHITE):
                self.remove_piece(square2)
                self.place_piece(square1, piece)  # put the piece back
                if piece2 is not None:
                    self.place_piece(square2, piece2)  # put the other piece back (if there was one)
                return False
            if not white_piece and self.king_in_check(self.BLACK):
                self.remove_piece(square2)
                self.place_piece(square1, piece)  # put the piece back
                if piece2 is not None:
                    self.place_piece(square2, piece2)  # put the other piece back (if there was one)
                return False

            piece.has_moved = True  # mark the piece has having moved
            return True
        else:
            return False

    def square_taken(self, square):
        return self.get_piece(square) is not None

    def square_taken_own_piece(self, square, current_piece):
        if self.square_taken(square):  # if square is taken by a piece of either color
            other_piece = self.get_piece(square)
            other_color = other_piece.color
            if current_piece.color == other_color:  # same color
                return True
            else:  # opposing colors
                return False
        else:
            return False  # no piece on that square

    def square_taken_opp_piece(self, square, current_piece):
        if self.square_taken(square):  # if square is taken by a piece of either color
            other_piece = self.get_piece(square)
            other_color = other_piece.color
            if current_piece.color != other_color:  # different color
                return True
            else:  # same colors
                return False
        else:
            return False  # no piece on that square

    def legal_move(self, square1, square2):
        if self.get_piece(square1) is not None:  # check that there is a piece on that square
            piece = self.get_piece(square1)  # get it
            color = piece.color
        else:
            return False

        if self.square_taken_own_piece(square2, piece):  # check if new square is taken by same color piece
            return False

        if piece.name == "Rook":
            return self.legal_rook_move(square1, square2, piece)

        elif piece.name == "King":
            if not piece.has_moved:
                return self.legal_king_move(square1, square2, piece) or self.legal_castle(square1, square2, piece)
            if piece.has_moved:
                return self.legal_king_move(square1, square2, piece)

        elif piece.name == "Pawn":
            return self.legal_pawn_move(square1, square2, piece) or self.legal_en_passant(square1, square2, piece)

        elif piece.name == "Knight":
            return self.legal_knight_move(square1, square2)

        elif piece.name == "Queen":
            return self.legal_queen_move(square1, square2, piece)

        elif piece.name == "Bishop":
            return self.legal_bishop_move(square1, square2, piece)

    def legal_pawn_move(self, square1, square2, pawn):
        x1 = square1[0]  # get coordinates
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]
        color = pawn.color  # get color

        # WHITE PAWN:_________________________________
        if color == self.WHITE:
            # Forward 2
            if not pawn.has_moved:
                # check its moving forward 2 and path is not blocked in either square
                if x2 == x1 and y2 == y1 + 2 and not self.square_taken((x1, y1 + 1)) and not self.square_taken(
                        (x1, y1 + 2)):
                    return True

            # Forward 1
            # either case (has moved/has not moved) included here, check s2 is forward 1 and is not taken
            if x2 == x1 and y2 == y1 + 1 and not self.square_taken((x1, y1 + 1)):
                return True

            # Capturing Diagonally
            if self.square_taken_opp_piece(square2, pawn) and (x2 == x1 + 1 or x2 == x1 - 1) and y2 == y1 + 1:
                return True

        # BLACK PAWN:__________________________________
        if color == self.BLACK:
            # Forward 2
            if not pawn.has_moved:
                # check its moving forward 2 and path is not blocked in either square
                if x2 == x1 and y2 == y1 - 2 and not self.square_taken((x1, y1 - 1)) and not self.square_taken(
                        (x1, y1 - 2)):
                    return True

            # Forward 1
            # either case (has moved/has not moved) included here, check s2 is forward 1 and is not taken
            if x2 == x1 and y2 == y1 - 1 and not self.square_taken((x1, y1 - 1)):
                return True

            # # Capturing Diagonally
            if self.square_taken_opp_piece(square2, pawn) and (x2 == x1 + 1 or x2 == x1 - 1) and y2 == y1 - 1:
                return True

        return False

    def legal_en_passant(self, square1, square2, piece):
        if piece.name != "Pawn" or len(self.move_list) == 0:  # check len!=0 so we dont pop from an empty list
            return False

        x1 = square1[0]  # get coordinates
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]

        previous_move = self.move_list[-1]  # get coordinates of previous move
        previous_square1 = previous_move[0]
        p_x1 = previous_square1[0]
        p_y1 = previous_square1[1]
        previous_square2 = previous_move[1]
        p_x2 = previous_square2[0]
        p_y2 = previous_square2[1]

        if piece.color == self.WHITE:
            if (x2 == x1 + 1 or x2 == x1 - 1) and y2 == 5:  # if diagonal move to 5th row
                if x2 == p_x1 == p_x2 and p_y1 == 6 and p_y2 == 4:  # check previous move was pawn push on same col
                    return True
        else:
            if (x2 == x1 + 1 or x2 == x1 - 1) and y2 == 2:  # if diagonal move to 2nd row
                if x2 == p_x1 == p_x2 and p_y1 == 1 and p_y2 == 3:  # check previous move was pawn push on same col
                    return True

    def en_passant(self, square1, square2, piece):
        # performs en passant moving pieces, have to call this after legal_en_passant (doesn't check if legal)
        x1 = square1[0]  # get coordinates
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]

        # move pawn diagonally
        self.remove_piece(square1)
        self.place_piece(square2, piece)  # no need for piece moved = True because it has to be true already
        # remove other pawn (2 cases)
        if piece.color == self.WHITE:
            self.remove_piece((x2, y2 - 1))
        else:
            self.remove_piece((x2, y2 + 1))

    def legal_king_move(self, square1, square2, piece):
        # get coordinates
        x1 = square1[0]
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]
        white_piece = piece.white_piece()

        # make sure king isn't moving into check
        if white_piece:
            if self.black_attacks[x2][y2] == 1:
                return False
        else:
            if self.white_attacks[x2][y2] == 1:
                return False

        delta_x = abs(x2 - x1)
        delta_y = abs(y2 - y1)

        if delta_x > 1 or delta_y > 1:
            return False
        else:
            return True

    def castle(self, square1, square2, piece):
        # move the pieces to castle (would have to call legal_castle before this)
        if square1 == (4, 0) and square2 == (6, 0):
            self.remove_piece(square1)
            self.place_piece(square2, piece)
            piece.has_moved = True
            rook = self.position[7][0]
            self.remove_piece((7, 0))
            self.place_piece((5, 0), rook)
            rook.has_moved = True

            # Queen-side Castling
        if square1 == (4, 0) and square2 == (1, 0) or square2 == (2, 0):
            self.remove_piece(square1)
            self.place_piece((2, 0), piece)
            piece.has_moved = True
            rook = self.position[0][0]
            self.remove_piece((0, 0))
            self.place_piece((3, 0), rook)
            rook.has_moved = True

        # Black king
        # king side castle
        if square1 == (4, 7) and square2 == (6, 7):
            self.remove_piece(square1)
            self.place_piece(square2, piece)
            piece.has_moved = True
            rook = self.position[7][7]
            self.remove_piece((7, 7))
            self.place_piece((5, 7), rook)
            rook.has_moved = True

        # Queen-side Castling
        if square1 == (4, 7) and square2 == (1, 7) or square2 == (2, 7):
            self.remove_piece(square1)  # have to move manually because move piece calls this
            self.place_piece((2, 7), piece)
            piece.has_moved = True
            rook = self.position[0][7]
            self.remove_piece((0, 7))
            self.place_piece((3, 7), rook)
            rook.has_moved = True

        return False

    def legal_castle(self, square1, square2, piece):
        # true if castling in this scenario is legal, false otherwise
        if piece.name != "King":
            return False

        # White King:
        if piece.color == self.WHITE:
            # King-side Castling
            king_moved = piece.has_moved
            rook_in_position = self.square_taken((7, 0)) and self.position[7][0].name == "Rook"
            if self.square_taken((7, 0)):  # TODO added this so we don't call .has_moved on None
                rook_moved = self.position[7][0].has_moved
            piece_blocking = self.square_taken((5, 0)) or self.square_taken((6, 0))
            check = self.black_attacks[4][0] == 1  # true if king is in check
            through_check = (self.black_attacks[5][0] or self.black_attacks[6][0]) == 1  # true if castle thu check

            if not king_moved and rook_in_position and not rook_moved and not piece_blocking and not check \
                    and not through_check:
                if square1 == (4, 0) and square2 == (6, 0):
                    return True

            # Queen-side Castling
            king_moved = piece.has_moved
            rook_in_position = self.square_taken((0, 0)) and self.position[0][0].name == "Rook"
            if self.square_taken((0, 0)):
                rook_moved = self.position[0][0].has_moved
            piece_blocking = self.square_taken((1, 0)) or self.square_taken((2, 0)) or self.square_taken((3, 0))
            check = self.black_attacks[4][0] == 1  # true if king is in check
            through_check = (self.black_attacks[2][0] or self.black_attacks[3][0]) == 1  # true if castle thu check

            if not king_moved and rook_in_position and not rook_moved and not piece_blocking and not check \
                    and not through_check:
                if square1 == (4, 0) and square2 == (1, 0) or square2 == (2, 0):
                    return True
        # Black king
        else:
            # King-side Castling
            king_moved = piece.has_moved
            rook_in_position = self.square_taken((7, 7)) and self.position[7][7].name == "Rook"
            if self.square_taken((7, 7)):
                rook_moved = self.position[7][7].has_moved
            piece_blocking = self.square_taken((5, 7)) or self.square_taken((6, 7))
            check = self.white_attacks[4][7] == 1  # true if king is in check
            through_check = (self.white_attacks[5][7] or self.white_attacks[6][7]) == 1  # true if castle thu check

            if not king_moved and rook_in_position and not rook_moved and not piece_blocking and not check \
                    and not through_check:
                if square1 == (4, 7) and square2 == (6, 7):
                    return True

            # Queen-side Castling
            king_moved = piece.has_moved
            rook_in_position = self.square_taken((0, 7)) and self.position[0][7].name == "Rook"
            if self.square_taken((0, 7)):
                rook_moved = self.position[0][7].has_moved
            piece_blocking = self.square_taken((1, 7)) or self.square_taken((2, 7)) or self.square_taken((3, 7))
            check = self.white_attacks[4][7] == 1  # true if king is in check
            through_check = (self.white_attacks[2][7] or self.white_attacks[3][7]) == 1  # true if castle thu check

            if not king_moved and rook_in_position and not rook_moved and not piece_blocking and not check \
                    and not through_check:
                if square1 == (4, 7) and square2 == (1, 7) or square2 == (2, 7):
                    return True
        return False

    def legal_rook_move(self, square1, square2, piece):
        # get coordinates
        x1 = square1[0]
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]
        if (x1 == x2 or y1 == y2) and not self.rook_collision(square1, square2):
            return True
        else:
            return False

    def rook_collision(self, square1, square2):
        # returns true if there is a collision, false otherwise
        # get coordinates
        x1 = square1[0]
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]

        piece = self.get_piece(square1)

        # 4 cases of rook moves:
        # up
        if x1 == x2 and y2 > y1:
            for i in range(y1+1, y2):
                if self.square_taken((x1, i)):
                    return True
        # down
        if x1 == x2 and y2 < y1:
            for i in range(y2 + 1, y1):
                if self.square_taken((x1, i)):
                    return True
        # right
        if y1 == y2 and x2 > x1:
            for i in range(x1 + 1, x2):
                if self.square_taken((i, y1)):
                    return True
        # left
        if y1 == y2 and x2 < x1:
            for i in range(x2 + 1 , x1):
                if self.square_taken((i, y1)):
                    return True

        return False

    def legal_knight_move(self, square1, square2):
        x1 = square1[0]
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]

        # 8 possible knight moves
        if (x2 == x1 + 1 and y2 == y1 + 2) or (x2 == x1 - 1 and y2 == y1 + 2) or (x2 == x1 + 1 and y2 == y1 - 2) or (
                x2 == x1 - 1 and y2 == y1 - 2) or \
                (x2 == x1 + 2 and y2 == y1 + 1) or (x2 == x1 + 2 and y2 == y1 - 1) or (
                x2 == x1 - 2 and y2 == y1 + 1) or (x2 == x1 - 2 and y2 == y1 - 1):
            return True
        else:
            return False

    def legal_bishop_move(self, square1, square2, piece):
        x1 = square1[0]
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]

        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)

        if delta_x == delta_y and not self.bishop_collision(square1, square2):
            return True
        else:
            return False

    def bishop_collision(self, square1, square2):
        # returns true if there is a collision, false otherwise
        # assume that we are given a diagonal move (legal bishop move takes care of that)
        # get coordinates
        x1 = square1[0]
        y1 = square1[1]
        x2 = square2[0]
        y2 = square2[1]

        # 4 CASES OF BISHOP MOVES: up-r, up-l, dwn-r, dwn-l
        # up-right
        if x2 - x1 > 0 and y2 - y1 > 0:
            # construct list of points in between
            x_points = []
            for i in range(x1 + 1, x2):
                x_points.append(i)
            y_points = []
            for i in range(y1 + 1, y2):
                y_points.append(i)
            # check each point
            for i in range(0, len(x_points)):
                if self.square_taken((x_points[i], y_points[i])):
                    return True

        # up-left
        if x2 - x1 < 0 and y2 - y1 > 0:
            # construct list of points in between
            x_points = []
            for i in range(x2 + 1, x1):
                x_points.append(i)
            x_points.reverse()
            y_points = []
            for i in range(y1 + 1, y2):
                y_points.append(i)
            # check each point
            for i in range(0, len(x_points)):
                if self.square_taken((x_points[i], y_points[i])):
                    return True

        # down-right
        if x2 - x1 > 0 and y2 - y1 < 0:
            # construct list of points in between
            x_points = []
            for i in range(x1 + 1, x2):
                x_points.append(i)
            y_points = []
            for i in range(y2 + 1, y1):
                y_points.append(i)
            y_points.reverse()
            # check each point
            for i in range(0, len(x_points)):
                if self.square_taken((x_points[i], y_points[i])):
                    return True

        # down-left
        if x2 - x1 < 0 and y2 - y1 < 0:
            # construct list of points in between
            x_points = []
            for i in range(x2 + 1, x1):
                x_points.append(i)
            y_points = []
            for i in range(y2 + 1, y1):
                y_points.append(i)
            # check each point
            for i in range(0, len(x_points)):
                if self.square_taken((x_points[i], y_points[i])):
                    return True

    def legal_queen_move(self, square1, square2, piece):
        if self.legal_bishop_move(square1, square2, piece) or self.legal_rook_move(square1, square2, piece):
            return True
        else:
            return False

    def piece_attacks(self, square):
        #  given the square a piece is on (assume there is a piece there) return all the other squares its attacking
        #  called it piece_attacks not piece moves, because pawn attacks and moves are different
        piece = self.get_piece(square)
        attacks = []
        if piece.name == "Pawn":  # pawns are special
            attacks = self.pawn_attacks(square)
        else:
            for i in range(0, 8):
                for j in range(0, 8):
                    if self.legal_move(square, (i, j)):
                        attacks.append((i, j))
        return attacks

    def pawn_attacks(self, square):
        # given there is a pawn on 'square'
        # get coordinates
        x = square[0]
        y = square[1]

        attacks = []
        piece = self.get_piece(square)
        if piece.white_piece():  # different for white and black pawns
            if y == 7:
                pass
            elif y == 0:
                pass
            elif x == 0:
                attacks.append((1, y + 1))  # pawn on left-most column
            elif x == 7:
                attacks.append((6, y + 1))  # pawn on right-most colum
            else:
                attacks.append((x + 1, y + 1))
                attacks.append((x - 1, y + 1))
        else:
            if x == 0:
                attacks.append((1, y - 1))
            elif x == 7:
                attacks.append((6, y - 1))
            else:
                attacks.append((x + 1, y - 1))
                attacks.append((x - 1, y - 1))
        return attacks

    def promotion(self, square2, color):
        # assume that the pawn has already made a legal move, we just want to check if its on the 8th rank
        piece = self.get_piece(square2)  # by the time we call this the piece has already moved to s2

        x2 = square2[0]
        y2 = square2[1]

        if self.square_taken(square2) and piece.name != "Pawn":
            return False

        if color == self.WHITE and y2 == 7:
            return True
        if color == self.BLACK and y2 == 0:
            return True

        return False

    def update_white_attacks(self):
        self.white_attacks = [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]]
        for i in range(0, 8):
            for j in range(0, 8):
                if self.square_taken((i, j)) and self.get_piece((i, j)).color == self.WHITE:
                    piece_attacks = self.piece_attacks((i, j))
                    for k in piece_attacks:
                        x = k[0]
                        y = k[1]
                        self.white_attacks[x][y] = 1

    def update_black_attacks(self):
        self.black_attacks = [[0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0]]
        for i in range(0, 8):
            for j in range(0, 8):
                if self.square_taken((i, j)) and self.get_piece((i, j)).color == self.BLACK:
                    piece_attacks = self.piece_attacks((i, j))
                    for k in piece_attacks:
                        x = k[0]
                        y = k[1]
                        self.black_attacks[x][y] = 1

    def illegal_move_pin(self, square1, square2):
        # if the piece can't move from square1 to square2 because of a pin (king would be in check) return true
        piece = self.get_piece(square1)
        if self.square_taken(square2):
            piece2 = self.get_piece(square2)  # if there is a piece on the 2nd square save it
        else:
            piece2 = None

        if piece.name == "King":  # none of this applies to the king
            return False

        # move the piece (manually because we don't want it to say it has moved)
        self.remove_piece(square1)
        self.place_piece(square2, piece)  # can still move if in a pin, just in the same direction

        self.update_white_attacks()
        self.update_black_attacks()  # i'm lazy so i just update both
        if self.king_in_check(piece.color):
            self.remove_piece(square2)
            self.place_piece(square1, piece)  # move the piece back
            if piece2 is not None:
                self.place_piece(square2, piece2)  # put the other piece back (if there was one)
            self.update_black_attacks()
            self.update_white_attacks()  # update attacks again
            return True  # true because the piece can't move because its in a pin
        else:
            self.remove_piece(square2)
            self.place_piece(square1, piece)
            if piece2 is not None:
                self.place_piece(square2, piece2)
            self.update_black_attacks()
            self.update_white_attacks()
            return False  # False because it is not pinned

    def king_in_check(self, color):
        # find king
        if self.find_king(color) is None:
            return False
        else:
            king_square = self.find_king(color)
        x = king_square[0]
        y = king_square[1]

        if color == self.WHITE:  # white king
            if self.black_attacks[x][y] == 1:
                return True
            else:
                return False
        else:  # black king
            if self.white_attacks[x][y] == 1:
                return True
            else:
                return False

    def find_king(self, color):
        for i in range(0, 8):
            for j in range(0, 8):
                if not self.square_taken((i, j)):
                    continue
                piece = self.get_piece((i, j))
                white = piece.white_piece()
                if piece.name == "King" and piece.color == color:
                    return i, j

    def checkmate(self, color):
        # returns true if that color's king is in checkmate
        king_square = self.find_king(color)
        king = self.get_piece(king_square)

        # check king is in check
        if not self.king_in_check(color):
            return False

        # check king has no legal moves
        for i in range(0, 8):
            for j in range(0, 8):
                square2 = i, j
                piece2 = self.get_piece(square2)

                if not self.legal_king_move(king_square, square2, king):  # don't even try if its not a legal king move
                    continue

                if self.square_taken_own_piece(square2, king):  # if its own piece is there it isn't legal
                    continue

                self.remove_piece(king_square)
                self.place_piece(square2, king)  # move the king to that square

                # if the king is still in check it is illegal. move the piece back and return false
                self.update_white_attacks()
                self.update_black_attacks()
                if color == self.WHITE and self.king_in_check(self.WHITE):  # king is in check
                    self.remove_piece(square2)
                    self.place_piece(king_square, king)  # put the piece back
                    if piece2 is not None:
                        self.place_piece(square2, piece2)  # put the other piece back (if there was one)
                elif color == self.WHITE and not self.king_in_check(self.WHITE):  # king is not in check
                    self.remove_piece(square2)
                    self.place_piece(king_square, king)
                    if piece2 is not None:
                        self.place_piece(square2, piece2)
                    return False  # return false because there is a legal king move

                if color == self.BLACK and self.king_in_check(self.BLACK):  # same with black
                    self.remove_piece(square2)
                    self.place_piece(king_square, king)
                    if piece2 is not None:
                        self.place_piece(square2, piece2)
                elif color == self.BLACK and not self.king_in_check(self.BLACK):
                    self.remove_piece(square2)
                    self.place_piece(king_square, king)
                    if piece2 is not None:
                        self.place_piece(square2, piece2)
                    return False

        # check none of the other pieces can block the check
        for i in range(0, 8):
            for j in range(0, 8):
                square1 = i, j
                if self.square_taken_own_piece(square1, king):
                    piece = self.get_piece(square1)
                else:
                    continue
                for k in range(0, 8):
                    for l in range(0, 8):
                        square2 = k, l
                        piece2 = self.get_piece(square2)

                        if not self.legal_move(square1, square2):  # don't even try if its not a legal king move
                            continue

                        if self.square_taken_own_piece(square2, king):  # if its own piece is there it isn't legal
                            continue

                        self.remove_piece(square1)
                        self.place_piece(square2, piece)  # move the king to that square

                        # if the king is still in check it is illegal. move the piece back and return false
                        self.update_white_attacks()
                        self.update_black_attacks()
                        if color == self.WHITE and self.king_in_check(self.WHITE):  # king is in check
                            self.remove_piece(square2)
                            self.place_piece(square1, piece)  # put the piece back
                            if piece2 is not None:
                                self.place_piece(square2, piece2)  # put the other piece back (if there was one)
                        elif color == self.WHITE and not self.king_in_check(self.WHITE):  # king is not in check
                            self.remove_piece(square2)
                            self.place_piece(square1, piece)
                            if piece2 is not None:
                                self.place_piece(square2, piece2)
                            print("legal move is: " + str(square1) + ", " + str(square2))
                            return False  # return false because there is a legal king move

                        if color == self.BLACK and self.king_in_check(self.BLACK):  # same with black
                            self.remove_piece(square2)
                            self.place_piece(square1, piece)
                            if piece2 is not None:
                                self.place_piece(square2, piece2)
                        elif color == self.BLACK and not self.king_in_check(self.BLACK):
                            self.remove_piece(square2)
                            self.place_piece(square1, piece)
                            if piece2 is not None:
                                self.place_piece(square2, piece2)
                            print("legal move is: " + str(square1) + ", " + str(square2))
                            return False

        return True

    def stalemate(self, color):
        # same code as checkmate but, king is not in check
        king_square = self.find_king(color)
        king = self.get_piece(king_square)

        # check king is in check
        if self.king_in_check(color):  # the one line that changed
            return False

        # check king has no legal moves
        for i in range(0, 8):
            for j in range(0, 8):
                square2 = i, j
                piece2 = self.get_piece(square2)

                if not self.legal_king_move(king_square, square2, king):  # don't even try if its not a legal king move
                    continue

                if self.square_taken_own_piece(square2, king):  # if its own piece is there it isn't legal
                    continue

                self.remove_piece(king_square)
                self.place_piece(square2, king)  # move the king to that square

                # if the king is still in check it is illegal. move the piece back and return false
                self.update_white_attacks()
                self.update_black_attacks()
                if color == self.WHITE and self.king_in_check(self.WHITE):  # king is in check
                    self.remove_piece(square2)
                    self.place_piece(king_square, king)  # put the piece back
                    if piece2 is not None:
                        self.place_piece(square2, piece2)  # put the other piece back (if there was one)
                elif color == self.WHITE and not self.king_in_check(self.WHITE):  # king is not in check
                    self.remove_piece(square2)
                    self.place_piece(king_square, king)
                    if piece2 is not None:
                        self.place_piece(square2, piece2)
                    return False  # return false because there is a legal king move

                if color == self.BLACK and self.king_in_check(self.BLACK):  # same with black
                    self.remove_piece(square2)
                    self.place_piece(king_square, king)
                    if piece2 is not None:
                        self.place_piece(square2, piece2)
                elif color == self.BLACK and not self.king_in_check(self.BLACK):
                    self.remove_piece(square2)
                    self.place_piece(king_square, king)
                    if piece2 is not None:
                        self.place_piece(square2, piece2)
                    return False

        # check none of the other pieces can block the check
        for i in range(0, 8):
            for j in range(0, 8):
                square1 = i, j
                if self.square_taken_own_piece(square1, king):
                    piece = self.get_piece(square1)
                else:
                    continue
                for k in range(0, 8):
                    for l in range(0, 8):
                        square2 = k, l
                        piece2 = self.get_piece(square2)

                        if not self.legal_move(square1, square2):  # don't even try if its not a legal king move
                            continue

                        if self.square_taken_own_piece(square2, king):  # if its own piece is there it isn't legal
                            continue

                        self.remove_piece(square1)
                        self.place_piece(square2, piece)  # move the king to that square

                        # if the king is still in check it is illegal. move the piece back and return false
                        self.update_white_attacks()
                        self.update_black_attacks()
                        if color == self.WHITE and self.king_in_check(self.WHITE):  # king is in check
                            self.remove_piece(square2)
                            self.place_piece(square1, piece)  # put the piece back
                            if piece2 is not None:
                                self.place_piece(square2, piece2)  # put the other piece back (if there was one)
                        elif color == self.WHITE and not self.king_in_check(self.WHITE):  # king is not in check
                            self.remove_piece(square2)
                            self.place_piece(square1, piece)
                            if piece2 is not None:
                                self.place_piece(square2, piece2)
                            print("legal move is: " + str(square1) + ", " + str(square2))
                            return False  # return false because there is a legal king move

                        if color == self.BLACK and self.king_in_check(self.BLACK):  # same with black
                            self.remove_piece(square2)
                            self.place_piece(square1, piece)
                            if piece2 is not None:
                                self.place_piece(square2, piece2)
                        elif color == self.BLACK and not self.king_in_check(self.BLACK):
                            self.remove_piece(square2)
                            self.place_piece(square1, piece)
                            if piece2 is not None:
                                self.place_piece(square2, piece2)
                            print("legal move is: " + str(square1) + ", " + str(square2))
                            return False

        return True

    def three_move_repetition(self):
        if len(self.move_list) <= 9:
            return False

        # most recent moves:
        one = self.move_list[-1]
        two = self.move_list[-2]
        three = self.move_list[-3]
        four = self.move_list[-4]
        five = self.move_list[-5]
        six = self.move_list[-6]
        seven = self.move_list[-7]
        eight = self.move_list[-8]

        if one == five and two == six and three == seven and four == eight:
            return True




