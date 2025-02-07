# src/pieces/king.py
from pieces.piece import Piece
from move import Move

class King(Piece):
    def get_moves(self, row, col):
        moves = []
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = "w" if self.white_to_move else "b"
        for move in king_moves:
            end_row = row + move[0]
            end_col = col + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally:
                    moves.append(Move((row, col), (end_row, end_col), self.board))
        return moves