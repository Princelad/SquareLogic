# src/pieces/rook.py
from pieces.piece import Piece
from move import Move

class Rook(Piece):
    def get_moves(self, row, col):
        moves = []
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy = "b" if self.white_to_move else "w"

        for d in direction:
            for i in range(1, 8):
                end_row = row + d[0] * i
                end_col = col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((row, col), (end_row, end_col), self.board))
                        break  # We can't jump the enemy piece
                    else:  # Friendly piece
                        break
                else:  # Out of board
                    break
        return moves