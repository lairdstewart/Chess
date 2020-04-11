# Chess

My first OOP Python project. My goal was to create a fully functioning two player chess game. The game supports castling, en-passant, check, checkmate, stalemate, three-move repetition, etc. 

Chess.py runs the pygame game loop, Board.py runs the back-end mechanics of the game, PygameClient.py contains the win, stalemate, promition, etc. messages. Each piece subclass contains its name, color, has-moved, get_color, and draw method. 

