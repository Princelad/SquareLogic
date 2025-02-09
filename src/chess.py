'''
Main driver file. Responsible for handling user input and displaying the current GameState object.
'''

import pygame as pg
from keymanager import KeyManager
import engine

# Constants for the window and chessboard
WIDTH = HEIGHT = 512
DIMENSION = 8  # Dimension of the chess board (8x8)
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 144  # For animations
IMAGES = {}


class chess():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.screen.fill(pg.Color("white"))
        self.running = True
        self.game_state = engine.GameState()
        self.load_images()  # Load the images
        self.key_manager = KeyManager()

    def run(self):
        pg.display.set_caption("Square Logic")
        valid_moves = self.game_state.get_valid_moves()
        move_made = False  # Flag that checks weather the user has made a move
        animate = False  # Flag that checks weather the user has made a move
        promotion_type = "Q"
        sq_selected = ()  # Keeps track of the selected square (row, col)
        player_clicks = []  # List of selected squares.

        while self.running:
            self.key_manager.handle_events()

            if self.key_manager.quit:
                self.running = False
            elif self.key_manager.mouse_button_down:
                # (x, y) position of the mouse
                mouse_pos = self.key_manager.mouse_pos
                col = mouse_pos[0] // SQ_SIZE
                row = mouse_pos[1] // SQ_SIZE

                if sq_selected == (row, col):  # Deselect square if clicked twice
                    sq_selected = ()
                    player_clicks = []
                elif self.game_state.board[row][col] != "--" or len(player_clicks) == 1:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                if len(player_clicks) == 2:  # After two clicks, make a move
                    move = engine.Move(
                        player_clicks[0], player_clicks[1], self.game_state.board)
                    print(move.get_chess_notation())
                    for i in range(len(valid_moves)):
                        '''
                        This allows us to use the move generated by the engine thus they can be more complex,
                        In the sense of the information about the move.Also keep the player moves simple and 
                        isolated.
                        '''
                        if move == valid_moves[i]:
                            if move.is_pawn_promotion:
                                self.game_state.make_move(
                                    valid_moves[i], promotion_type)
                            else:
                                self.game_state.make_move(valid_moves[i])
                            move_made = True
                            animate = True
                            sq_selected = ()  # Reset user selection
                            player_clicks = []
                    if not move_made:
                        player_clicks = [sq_selected]
            # Handles the keys.
            elif self.key_manager.backspace_pressed:
                self.game_state.undo_move()
                move_made = True
                animate = False
            elif self.key_manager.reset_pressed:
                self.game_state = engine.GameState()
                valid_moves = self.game_state.get_valid_moves()
                sq_selected = ()
                player_clicks = []
                move_made = False
                animate = False

            mouse_pos = pg.mouse.get_pos()
            hover_square = (mouse_pos[1] // SQ_SIZE, mouse_pos[0] // SQ_SIZE)

            self.draw_game_state(hover_square, sq_selected, valid_moves, self.game_state.move_log[-1] if len(
                self.game_state.move_log) != 0 else None)
            self.clock.tick(MAX_FPS)
            pg.display.flip()

            if move_made:
                if animate:
                    self.animate_move(
                        self.game_state.move_log[-1])
                valid_moves = self.game_state.get_valid_moves()
                move_made = False

        pg.quit()

    def load_images(self):
        pieces = ["wP", "wR", "wN", "wB", "wQ",
                  "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
        for piece in pieces:
            IMAGES[piece] = pg.transform.scale(
                pg.image.load("assets/pieces/" + piece +
                              ".png"), (SQ_SIZE, SQ_SIZE)
            )

    # Responsible for rendering the game state
    def draw_game_state(self, hover_square, sq_selected, valid_moves, last_move=None):
        self.draw_board(hover_square)  # Draw the squares
        self.highlight_squares(valid_moves, sq_selected)
        self.last_move_made(last_move)
        # Draw the pieces on top of the squares
        self.draw_pieces()

    # Draw the board (alternating colors)
    def draw_board(self, hover_square=None):
        global colors
        colors = [pg.Color(255, 206, 158), pg.Color(209, 139, 71)]

        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[(row + col) % 2]

                pg.draw.rect(self.screen, color, pg.Rect(
                    col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

                # Highlight hover square
                if hover_square == (row, col):
                    pg.draw.rect(self.screen, pg.Color(255, 255, 100, 100),
                                 pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)

    # Draw the pieces on the board
    def draw_pieces(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = self.game_state.board[row][col]
                if piece != "--":  # If not an empty square
                    self.screen.blit(IMAGES[piece], pg.Rect(
                        col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Draw moves and selected square
    def highlight_squares(self, valid_moves, sq_selected):
        if sq_selected != ():
            r, c = sq_selected
            if self.game_state.board[r][c][0] == ("w" if self.game_state.white_to_move else "b"):
                # Highlight selected square with a yellowish tint
                pg.draw.rect(self.screen, pg.Color(255, 255, 100, 100),
                             (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)

                # Highlight valid move destinations with a grayish circle
                for move in valid_moves:
                    if move.start_row == r and move.start_col == c:
                        center = ((move.end_col * SQ_SIZE) + SQ_SIZE //
                                  2, (move.end_row * SQ_SIZE) + SQ_SIZE // 2)
                        radius = SQ_SIZE // 6  # Small indicator in the center
                        pg.draw.circle(self.screen, pg.Color(
                            255, 255, 100, 100), center, radius)

    # Highlight the last move made
    def last_move_made(self, move):
        if move is not None:
            start_square = pg.Rect(
                move.start_col * SQ_SIZE, move.start_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            end_square = pg.Rect(move.end_col * SQ_SIZE,
                                 move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            # Reddish color for highlighting
            highlight_color = pg.Color(255, 0, 0, 100)

            pg.draw.rect(self.screen, highlight_color, start_square)
            pg.draw.rect(self.screen, highlight_color, end_square)

    # Move animation
    def animate_move(self, move):
        global colors
        dR = move.end_row - move.start_row
        dC = move.end_col - move.start_col
        frames_per_square = 20  # Frames to move one square
        frames_count = (abs(dR) + abs(dC)) * frames_per_square
        for frame in range(frames_count + 1):
            r, c = (move.start_row + dR * frame / frames_count,
                    move.start_col + dC * frame / frames_count)
            self.draw_board()
            self.draw_pieces()
            # Erase the piece from the ending square
            color = colors[(move.end_row + move.end_col) % 2]
            end_square = pg.Rect(
                move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pg.draw.rect(self.screen, color, end_square)
            # Draw captured piece back
            if move.piece_captured != "--":
                self.screen.blit(IMAGES[move.piece_captured], end_square)
            # Draw moving piece
            self.screen.blit(IMAGES[move.piece_moved], pg.Rect(
                int(c * SQ_SIZE), int(r * SQ_SIZE), SQ_SIZE, SQ_SIZE))
            pg.display.flip()
            self.clock.tick(MAX_FPS)
