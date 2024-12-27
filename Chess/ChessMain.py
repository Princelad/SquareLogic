import pygame as pg

from Chess import ChessEngine

WIDTH = HEIGHT = 512

DIMENSION = 8

SQ_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15

IMAGES = {}

def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    screen.fill(pg.Color("white"))
    game_state = ChessEngine.GameState()

    load_images()

    running = True

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        pg.display.flip()

def draw_game_state(screen, game_state):
    draw_board(screen)
    draw_pieces(screen, game_state.board)

def draw_board(screen):
    colors = [pg.Color("white"), pg.Color("gray")]

    for rows in range(DIMENSION):
        for cols in range(DIMENSION):
            color = colors[(rows + cols) % 2]
            pg.draw.rect(screen, color, pg.Rect(cols * SQ_SIZE, rows * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces(screen, board):
    for rows in range(DIMENSION):
        for cols in range(DIMENSION):
            piece = board[rows][cols]

            if piece != "--" :
                screen.blit(IMAGES[piece], pg.Rect(cols * SQ_SIZE, rows * SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
