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
                            sq_selected = ()  # Reset user selection
                            player_clicks = []
                    if not move_made:
                        player_clicks = [sq_selected]
            # Handles the keys.
            elif self.key_manager.backspace_pressed:
                self.game_state.undo_move()
                move_made = True

            mouse_pos = pg.mouse.get_pos()
            hover_square = (mouse_pos[1] // SQ_SIZE, mouse_pos[0] // SQ_SIZE)

            self.draw_game_state(self.screen, self.game_state,
                                 hover_square, sq_selected, valid_moves)
            self.clock.tick(MAX_FPS)
            pg.display.flip()

            if move_made:
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
    def draw_game_state(self, screen, game_state, hover_square, sq_selected, valid_moves):
        self.draw_board(screen, hover_square)  # Draw the squares
        self.highlight_squares(screen, game_state, valid_moves, sq_selected)
        # Draw the pieces on top of the squares
        self.draw_pieces(screen, game_state.board)

    # Draw the board (alternating colors)
    def draw_board(self, screen, hover_square):
        colors = [pg.Color(255, 206, 158), pg.Color(209, 139, 71)]

        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[(row + col) % 2]

                pg.draw.rect(screen, color, pg.Rect(
                    col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

                # Highlight hover square
                if hover_square == (row, col):
                    pg.draw.rect(screen, pg.Color(255, 255, 100, 100),
                                 pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE), 3)

    # Draw the pieces on the board
    def draw_pieces(self, screen, board):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece = board[row][col]
                if piece != "--":  # If not an empty square
                    screen.blit(IMAGES[piece], pg.Rect(
                        col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

    # Draw moves and selected square
    def highlight_squares(self, screen, game_state, valid_moves, sq_selected):
        if sq_selected != ():
            r, c = sq_selected
            if game_state.board[r][c][0] == ("w" if game_state.white_to_move else "b"):
                # Highlight selected square with a yellowish tint
                pg.draw.rect(screen, pg.Color(255, 255, 100, 100),
                             (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 0)

                # Highlight valid move destinations with a grayish circle
                for move in valid_moves:
                    if move.start_row == r and move.start_col == c:
                        center = ((move.end_col * SQ_SIZE) + SQ_SIZE //
                                  2, (move.end_row * SQ_SIZE) + SQ_SIZE // 2)
                        radius = SQ_SIZE // 6  # Small indicator in the center
                        pg.draw.circle(screen, pg.Color(
                            255, 255, 100, 100), center, radius)

    # Move animation
    def animate_move(self, screen, game_state, move, clock):
        pass
