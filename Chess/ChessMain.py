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
    gs = ChessEngine.GameState()



main()
