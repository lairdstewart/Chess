from Pieces.Piece import Piece
import pygame
from DrawHelper import DrawHelper


class Queen(Piece):
    name = "Queen"

    def __init__(self, color):
        super().__init__(color)

    def draw(self, screen, x, y, square_size):
        tenth = square_size/10
        twentieth = square_size/20

        # define 11 points that make the queen's polygon
        one = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 1))
        two = DrawHelper.scale_coordinates(square_size, x, y, (3.5, 6))
        three = DrawHelper.scale_coordinates(square_size, x, y, (3, 8))
        four = DrawHelper.scale_coordinates(square_size, x, y, (5, 6))
        five = DrawHelper.scale_coordinates(square_size, x, y, (4, 7))
        six = DrawHelper.scale_coordinates(square_size, x, y, (5, 8))
        seven = DrawHelper.scale_coordinates(square_size, x, y, (6, 7))
        eight = four
        nine = DrawHelper.scale_coordinates(square_size, x, y, (7, 8))
        ten = DrawHelper.scale_coordinates(square_size, x, y, (6.5, 6))
        eleven = DrawHelper.scale_coordinates(square_size, x, y, (6.5, 1))
        twelve = one

        # draw shape
        pygame.draw.polygon(screen, self.color, (
            one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve))

        # draw outline
        pygame.draw.polygon(screen, self.opposite_color, (
            one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve), 2)

        # draw circle on top
        pygame.draw.circle(screen, self.color, (x + 5*tenth, y + 2*tenth), 0.5*tenth)
        pygame.draw.circle(screen, self.opposite_color, (x + 5*tenth, y + 2*tenth), 0.5*tenth, 2)  # outline
