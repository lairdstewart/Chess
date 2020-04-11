class Piece:
    name = ""
    has_moved = False  # need this for pawn moves, castling, etc.

    def __init__(self, color):
        if color == 1:
            self.color = (255, 255, 255)  # white
            self.opposite_color = (0, 0, 0)
        else:
            self.color = (0, 0, 0)  # black
            self.opposite_color = (255, 255, 255)

    def draw(self, screen, x, y, square_size):
        pass

    def white_piece(self):
        # true if white, false if black
        if self.color == (255, 255, 255):
            return True
        else:
            return False

    def black_piece(self):
        # true if black, false if white
        if self.color == (0, 0, 0):
            return True
        else:
            return False






