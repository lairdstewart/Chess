import pygame


class DrawHelper:
    @staticmethod
    def scale_coordinates(square_size, x, y, coordinates):
        # x, y are top left of the square to draw in
        x_cord = coordinates[0]
        y_cord = coordinates[1]
        y_cord = 10 - y_cord  # pygame starts in top left, my coordinates in standard form

        tenth = square_size/10

        return x + x_cord*tenth, y + y_cord*tenth
