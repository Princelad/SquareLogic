"""
This is the main driver file. Includes loading of different objects.
"""

import pygame as pg
import numpy as np
from Chess import ChessEngine

# Constants for the window and chessboard
WIDTH = HEIGHT = 512
DIMENSION = 8  # Dimension of the chess board (8x8)
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # For animations
IMAGES = {}

# Responsible for loading the images into the dictionary
def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(
            pg.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)
        )

# Main driver function
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    game_state = ChessEngine.GameState()
    load_images()  # Load the images

    running = True
    sq_selected = ()  # Keeps track of the selected square (row, col)
    player_clicks = []  # List of selected squares

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()  # (x, y) position of the mouse
                col = mouse_pos[0] // SQ_SIZE
                row = mouse_pos[1] // SQ_SIZE

                if sq_selected == (row, col):  # Deselect square if clicked twice
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)

                if len(player_clicks) == 2:  # After two clicks, make a move
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                    print(move.get_chess_notation())
                    game_state.make_move(move)
                    sq_selected = ()  # Reset user selection
                    player_clicks = []

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        pg.display.flip()

# Responsible for rendering the game state
def draw_game_state(screen, game_state):
    draw_board(screen)  # Draw the squares
    draw_pieces(screen, game_state.board)  # Draw the pieces on top of the squares

# Draw the board (alternating colors)
def draw_board(screen):
    colors = [pg.Color("white"), pg.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            pg.draw.rect(screen, color, pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw the pieces on the board
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":  # If not an empty square
                screen.blit(IMAGES[piece], pg.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
