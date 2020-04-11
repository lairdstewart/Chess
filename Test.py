from Chess import Chess
from Board import Board
import pygame
from Pieces.Rook import Rook
from Pieces.King import King
from Pieces.Pawn import Pawn
from Pieces.Knight import Knight
from Pieces.Queen import Queen
from Pieces.Bishop import Bishop
import time

chess = Chess()
chess.game()

# manual testing

# test_board = Board(640)
# test_board.draw_board()
#
# test_board.win_message((0, 0, 0))
# test_board.new_game_message()
#
# #
# # black_rook = Rook(0)
# # white_rook = Rook(1)
# # white_king = King(1)
# # black_king = King(0)
# # white_pawn = Pawn(1)
# # black_pawn = Pawn(0)
# #
# #
# # test_board.place_piece((1, 1), white_king)
# # test_board.place_piece((7, 7), black_king)
# # test_board.place_piece((1, 2), white_rook)
# # test_board.place_piece((1, 5), black_rook)
# # test_board.place_piece((2, 4), white_pawn)
# # test_board.place_piece((3, 5), black_pawn)
# #
# #
# done = True
# promotion = False
# selection = []
# while done is True:
#     pygame.display.flip()
#     for event in pygame.event.get():  # User did something
#         if event.type == pygame.QUIT:  # If user clicked close
#             done = False  # exit while loop
#
#         if event.type == pygame.MOUSEBUTTONDOWN and not promotion:  # normal move
#             if pygame.mouse.get_pressed()[0]:  # left mouse button pressed
#                 pos = pygame.mouse.get_pos()
#                 square = test_board.get_square(pos)
#                 selection.append(square)
#                 test_board.select_piece(square)
#                 pygame.display.flip()
#
#         if event.type == pygame.MOUSEBUTTONDOWN and promotion:  # promotion dialogue
#             if pygame.mouse.get_pressed()[0]:  # left mouse button pressed
#                 pos = pygame.mouse.get_pos()
#
#                 # Each box for each piece selection, if they don't press on the box, promotion is still true try again
#                 if 1.5*64 <= pos[0] < 2.5*64 and 1.5*64 <= pos[1] <= 2.5*64:
#                     knight = Knight(color)
#                     test_board.place_piece(square, knight)
#                     test_board.deselect_board()
#                     pygame.display.flip()
#                     promotion = False
#                 elif 3.5*64 <= pos[0] < 4.5*64 and 1.5*64 <= pos[1] <= 2.5*64:
#                     bishop = Bishop(color)
#                     test_board.place_piece(square, bishop)
#                     test_board.deselect_board()
#                     pygame.display.flip()
#                     promotion = False
#                 elif 5.5*64 <= pos[0] < 6.5*64 and 1.5*64 <= pos[1] <= 2.5*64:
#                     rook = Rook(color)
#                     test_board.place_piece(square, rook)
#                     test_board.deselect_board()
#                     pygame.display.flip()
#                     promotion = False
#                 elif 7.5*64 <= pos[0] < 8.5*64 and 1.5*64 <= pos[1] <= 2.5*64:
#                     queen = Queen(color)
#                     test_board.place_piece(square, queen)
#                     test_board.deselect_board()
#                     pygame.display.flip()
#                     promotion = False
#
#     if len(selection) == 2:
#         output = test_board.player_move(selection[0], selection[1])
#         selection = []
#         if output[0] == "Promotion":
#             color = output[1]
#             square = output[2]
#             test_board.promotion_message(color)
#             pygame.display.flip()
#             promotion = True
# #
# #
# #
# #
# #
#
#
