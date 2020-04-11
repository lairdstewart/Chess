import pygame
from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.Rook import Rook
from Pieces.Queen import Queen

class PygameClient:
    pygame.init()
    pygame.display.set_caption("Chess")
    font = pygame.font.SysFont('Calibri', 50, True, False)
    clock = pygame.time.Clock()

    GREEN = (100, 134, 68)  # default colors
    DARK_GREEN = (80, 114, 48)
    OFF_WHITE = (234, 235, 200)
    DARK_OFF_WHITE = (214, 215, 180)
    LIGHT_GRAY = (195, 195, 195)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    LIGHT_RED = (208, 105, 95)
    square_color = GREEN
    background_color = OFF_WHITE

    def __init__(self, size):  # for now just takes size (could include colors later)
        self.size = size
        self.square_size = size/8
        self.screen = pygame.display.set_mode((self.size, self.size))
        self.screen.fill(self.background_color)

    def coordinates_to_pygame_axis(self, coordinates):
        x = coordinates[0]
        y = coordinates[1]
        x = x * self.square_size
        y = 7 - y
        y = y * self.square_size
        return x, y

    def win_message(self, winning_color):
        if winning_color == self.WHITE:
            message = "WHITE WINS!"
        else:
            message = "BLACK WINS!"

        tenth = self.size / 10

        pygame.draw.rect(self.screen, self.WHITE, [2*tenth, 2*tenth, 6*tenth, 1.5*tenth])
        pygame.draw.rect(self.screen, self.BLACK, [2*tenth, 2*tenth, 6*tenth, 1.5*tenth], 3)

        text = self.font.render(message, True, self.BLACK)
        self.screen.blit(text, [3*tenth, 2.5*tenth])

    def promotion_message(self, color):
        if color == self.BLACK:
            color = 0
        else:
            color = 1

        knight = Knight(color)
        bishop = Bishop(color)
        rook = Rook(color)
        queen = Queen(color)

        tenth = self.size / 10
        pygame.draw.rect(self.screen, self.WHITE, [tenth, tenth, 8*tenth, 2*tenth])  # draw outer background
        pygame.draw.rect(self.screen, self.BLACK, [tenth, tenth, 8*tenth, 2*tenth], 5)  # draw outer background

        knight.draw(self.screen, 1.5*tenth, 1.5*tenth, tenth)
        pygame.draw.rect(self.screen, self.BLACK, [1.5*tenth, 1.5*tenth, tenth, tenth], 3)

        bishop.draw(self.screen, 3.5*tenth, 1.5*tenth, tenth)
        pygame.draw.rect(self.screen, self.BLACK, [3.5*tenth, 1.5*tenth, tenth, tenth], 3)

        rook.draw(self.screen, 5.5*tenth, 1.5*tenth, tenth)
        pygame.draw.rect(self.screen, self.BLACK, [5.5*tenth, 1.5*tenth, tenth, tenth], 3)

        queen.draw(self.screen, 7.5*tenth, 1.5*tenth, tenth)
        pygame.draw.rect(self.screen, self.BLACK, [7.5*tenth, 1.5*tenth, tenth, tenth], 3)

    def stalemate_message(self):
        message = "STALEMATE!"

        tenth = self.size / 10

        pygame.draw.rect(self.screen, self.WHITE, [2*tenth, 2*tenth, 6*tenth, 1.5*tenth])
        pygame.draw.rect(self.screen, self.BLACK, [2*tenth, 2*tenth, 6*tenth, 1.5*tenth], 3)

        text = self.font.render(message, True, self.BLACK)
        self.screen.blit(text, [3*tenth, 2.5*tenth])

    def new_game_message(self):
        tenth = self.size / 10

        # main box
        pygame.draw.rect(self.screen, self.WHITE, [2*tenth, 5*tenth, 6*tenth, 4*tenth])
        pygame.draw.rect(self.screen, self.BLACK, [2*tenth, 5*tenth, 6*tenth, 4*tenth], 3)

        # yes button
        pygame.draw.rect(self.screen, self.GREEN, [3*tenth, 7*tenth, 1.5*tenth, 1*tenth])
        pygame.draw.rect(self.screen, self.BLACK, [3*tenth, 7*tenth, 1.5*tenth, 1*tenth], 2)

        # check
        pygame.draw.line(self.screen, self.BLACK, (3.5*tenth, 7.5*tenth), (3.7*tenth, 7.7*tenth), 8)
        pygame.draw.line(self.screen, self.BLACK, (3.7*tenth, 7.7*tenth), (4*tenth, 7.3*tenth), 8)

        # no button
        pygame.draw.rect(self.screen, self.LIGHT_RED, [5.5*tenth, 7*tenth, 1.5*tenth, 1*tenth])
        pygame.draw.rect(self.screen, self.BLACK, [5.5*tenth, 7*tenth, 1.5*tenth, 1*tenth], 2)

        # x
        pygame.draw.line(self.screen, self.BLACK, (6*tenth, 7.3*tenth), (6.5*tenth, 7.7*tenth), 8)
        pygame.draw.line(self.screen, self.BLACK, (6.5*tenth, 7.3*tenth), (6*tenth, 7.7*tenth), 8)



        text = self.font.render("New Game?", True, self.BLACK)
        self.screen.blit(text, [3*tenth, 5.5*tenth])

    def three_move_repetition_message(self):
        message = "3 Move Repetition!"

        tenth = self.size / 10

        pygame.draw.rect(self.screen, self.WHITE, [2*tenth, 2*tenth, 6*tenth, 1.5*tenth])
        pygame.draw.rect(self.screen, self.BLACK, [2*tenth, 2*tenth, 6*tenth, 1.5*tenth], 3)

        text = self.font.render(message, True, self.BLACK)
        self.screen.blit(text, [2.2*tenth, 2.5*tenth])













