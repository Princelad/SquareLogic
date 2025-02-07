# src/pieces/piece.py
class Piece:
    def __init__(self, board, white_to_move):
        self.board = board
        self.white_to_move = white_to_move

    def get_moves(self, row, col):
        raise NotImplementedError("This method should be overridden by subclasses")