from Pieces.Piece import Piece
import pygame
from DrawHelper import DrawHelper


class Knight(Piece):
    name = "Knight"

    def __init__(self, color):
        super().__init__(color)

    def draw(self, screen, x, y, square_size):
        tenth = square_size/10

        # knight shape polygon
        p1 = DrawHelper.scale_coordinates(square_size, x, y, (6.5, 2))
        p2 = DrawHelper.scale_coordinates(square_size, x, y, (6.5, 4))
        p3 = DrawHelper.scale_coordinates(square_size, x, y, (7, 5))
        p4 = DrawHelper.scale_coordinates(square_size, x, y, (7, 8))
        p5 = DrawHelper.scale_coordinates(square_size, x, y, (6, 9))
        p6 = DrawHelper.scale_coordinates(square_size, x, y, (6, 9.5))
        p7 = DrawHelper.scale_coordinates(square_size, x, y, (5, 8.5))
        p8 = DrawHelper.scale_coordinates(square_size, x, y, (2, 7))
        p9 = DrawHelper.scale_coordinates(square_size, x, y, (2, 5))
        p10 = DrawHelper.scale_coordinates(square_size, x, y, (3, 5))
        p11 = DrawHelper.scale_coordinates(square_size, x, y, (5, 6))
        p12 = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 4))
        p13 = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 2))
        p14 = p1

        pygame.draw.polygon(screen, self.color, (p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14))
        pygame.draw.polygon(screen, self.opposite_color, (
            p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14), 2)

        # base rectangle
        pygame.draw.rect(screen, self.color, (x+3*tenth, y+8*tenth, 4*tenth, tenth))
        pygame.draw.rect(screen, self.opposite_color, (x+3*tenth, y+8*tenth, 4*tenth, tenth), 2)

        # eye
        eye_coordinate = DrawHelper.scale_coordinates(square_size, x, y, (4.5, 7))
        pygame.draw.circle(screen, self.opposite_color, eye_coordinate, 0.3*tenth)


