import pygame
from Pieces.Piece import Piece


class King(Piece):
    name = "King"

    def __init__(self, color):
        super().__init__(color)

    def draw(self, screen, x, y, square_size):
        # x and y here are the top left axis coordinates of the square
        tenth = square_size/10
        twentieth = square_size/20

        # main square
        pygame.draw.rect(screen, self.color, (x+3*tenth, y+4*tenth, 4*tenth, 5*tenth))
        pygame.draw.rect(screen, self.opposite_color, (x+3*tenth, y+4*tenth, 4*tenth, 5*tenth), 2)

        # draw lines in main square
        pygame.draw.line(screen, self.opposite_color, (x+7*twentieth, y + 5*tenth), (x+7*twentieth, y+9*tenth))
        pygame.draw.line(screen, self.opposite_color, (x+13*twentieth, y + 5*tenth), (x+13*twentieth, y+9*tenth))

        # draw horizontal cross part
        pygame.draw.rect(screen, self.color, (x+7*twentieth, y+2*tenth, 3*tenth, 1*tenth))
        pygame.draw.rect(screen, self.opposite_color, (x+7*twentieth, y+2*tenth, 3*tenth, 1*tenth), 2)

        # draw vertical cross part
        pygame.draw.rect(screen, self.color, (x+9*twentieth, y+tenth, 1*tenth, 3*tenth))
        pygame.draw.rect(screen, self.opposite_color, (x+9*twentieth, y+tenth, 1*tenth, 3*tenth), 2)




