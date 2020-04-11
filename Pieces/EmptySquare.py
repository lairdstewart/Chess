from Pieces.Piece import Piece


class EmptySquare(Piece):
    def __init__(self):
        self.name = None
        self.has_moved = None
        self.color = None
        self.opposite_color = None

    def draw(self, a, b, c, d):
        return  # an empty piece does nothing when asked to draw itself
