import pygame
from Pieces.Piece import Piece
from DrawHelper import DrawHelper


class Rook(Piece):
    name = "Rook"

    def __init__(self, color):
        super().__init__(color)

    def draw(self, screen, x, y, square_size):
        tenth = square_size/10
        # points to construct polynomial
        p1 = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 2))
        p2 = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 7))
        p3 = DrawHelper.scale_coordinates(square_size, x, y, (2.5, 7))
        p4 = DrawHelper.scale_coordinates(square_size, x, y, (2.5, 8.5))
        p5 = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 8.5))
        p6 = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 7.75))
        p7 = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 7.75))
        p8 = DrawHelper.scale_coordinates(square_size, x, y, (4.5, 7.75))
        p9 = DrawHelper.scale_coordinates(square_size, x, y, (4.5, 8.5))
        p10 = DrawHelper.scale_coordinates(square_size, x, y, (5.5, 8.5))
        p11 = DrawHelper.scale_coordinates(square_size, x, y, (5.5, 7.75))
        p12 = DrawHelper.scale_coordinates(square_size, x, y, (6.5, 7.75))
        p13 = DrawHelper.scale_coordinates(square_size, x, y, (6.5, 8.5))
        p14 = DrawHelper.scale_coordinates(square_size, x, y, (7.5, 8.5))
        p15 = DrawHelper.scale_coordinates(square_size, x, y, (7.5, 7))
        p16 = DrawHelper.scale_coordinates(square_size, x, y, (6.5, 7))
        p17 = DrawHelper.scale_coordinates(square_size, x, y, (6.5, 2))

        pygame.draw.polygon(screen, self.color, (
            p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17))
        pygame.draw.polygon(screen, self.opposite_color, (
            p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17), 2)

        # base rectangle
        pygame.draw.rect(screen, self.color, (x+2.5*tenth, y+8*tenth, 5*tenth, tenth))
        pygame.draw.rect(screen, self.opposite_color, (x+2.5*tenth, y+8*tenth, 5*tenth, tenth), 2)


