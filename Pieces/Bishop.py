from Pieces.Piece import Piece
import pygame
from DrawHelper import DrawHelper


class Bishop(Piece):
    name = "Bishop"

    def __init__(self, color):
        super().__init__(color)

    def draw(self, screen, x, y, square_size):
        tenth = square_size/10
        twentieth = square_size/20

        # bottom rectangle
        pygame.draw.rect(screen, self.color, (x+3*tenth, y+8*tenth, 4*tenth, tenth))
        pygame.draw.rect(screen, self.opposite_color, (x+3*tenth, y+8*tenth, 4*tenth, tenth), 2)

        # main polygon
        p1 = DrawHelper.scale_coordinates(square_size, x, y, (4, 2))
        p2 = DrawHelper.scale_coordinates(square_size, x, y, (4, 4))
        p3 = DrawHelper.scale_coordinates(square_size, x, y, (3, 7))
        p4 = DrawHelper.scale_coordinates(square_size, x, y, (5, 9))
        p5 = DrawHelper.scale_coordinates(square_size, x, y, (7, 7))
        p6 = DrawHelper.scale_coordinates(square_size, x, y, (6, 4))
        p7 = DrawHelper.scale_coordinates(square_size, x, y, (6, 2))
        p8 = p1

        pygame.draw.polygon(screen, self.color, (p1, p2, p3, p4, p5, p6, p7, p8))

        pygame.draw.polygon(screen, self.opposite_color, (p1, p2, p3, p4, p5, p6, p7, p8), 2)

        # little circle on top
        pygame.draw.circle(screen, self.opposite_color, (x + 5*tenth, y + 1*tenth), 0.5*tenth)
        pygame.draw.circle(screen, self.color, (x + 5*tenth, y + 1*tenth), 0.5*tenth, 2)  # outline

        # middle cross
        p1 = DrawHelper.scale_coordinates(square_size, x, y, (5, 7.5))
        p2 = DrawHelper.scale_coordinates(square_size, x, y, (5, 4.5))
        pygame.draw.line(screen, self.opposite_color, p1, p2, 2)

        p1 = DrawHelper.scale_coordinates(square_size, x, y, (4, 6.5))
        p2 = DrawHelper.scale_coordinates(square_size, x, y, (6, 6.5))
        pygame.draw.line(screen, self.opposite_color, p1, p2, 2)




