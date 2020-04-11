import pygame
from Pieces.Piece import Piece


class Pawn(Piece):
    name = "Pawn"

    def __init__(self, color):
        super().__init__(color)

    def draw(self, screen, x, y, square_size):
        # x and y here are the top left axis coordinates of the square
        tenth = square_size/10
        twentieth = square_size/20

        # base rectangle
        pygame.draw.rect(screen, self.color, (x+3*tenth, y+8*tenth, 4*tenth, tenth))
        pygame.draw.rect(screen, self.opposite_color, (x+3*tenth, y+8*tenth, 4*tenth, tenth), 2)

        # middle rectangle
        pygame.draw.rect(screen, self.color, (x+4*tenth, y+5*tenth, 2*tenth, 3*tenth))
        pygame.draw.rect(screen, self.opposite_color, (x+4*tenth, y+5*tenth, 2*tenth, 3*tenth), 2)

        # top circle
        pygame.draw.circle(screen, self.color, (x+5*tenth, y+4*tenth), 1.5*tenth)
        pygame.draw.circle(screen, self.opposite_color, (x+5*tenth, y+4*tenth), 1.5*tenth, 2)







