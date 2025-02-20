'''
Pawn class generates all possible moves for a pawn piece on the board.
'''

from pieces.piece import Piece
from move import Move


class Pawn(Piece):
    def __init__(self, board, white_to_move, enpassant_possible):
        super().__init__(board, white_to_move)
        self.enpassant_possible = enpassant_possible

    def get_moves(self, row, col):
        if row + 1 <= 7:
            moves = []
            if self.white_to_move:
                if self.board[row - 1][col] == "--":  # One square pawn advance
                    moves.append(Move((row, col), (row - 1, col), self.board))
                    # Two square pawn advance
                    if row == 6 and self.board[row - 2][col] == "--":
                        moves.append(Move((row, col), (row - 2, col), self.board))

                # Captures to the left
                # Enemy piece on the diagonal
                if col - 1 >= 0 and self.board[row - 1][col - 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col - 1), self.board))
                # Possible enpassant
                elif col - 1 >= 0 and (row - 1, col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - 1, col - 1),
                                self.board, is_enpassant=True))

                # Captures to the right
                if col + 1 <= 7 and self.board[row - 1][col + 1][0] == "b":
                    moves.append(Move((row, col), (row - 1, col + 1), self.board))
                elif col + 1 <= 7 and (row - 1, col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row - 1, col + 1),
                                self.board, is_enpassant=True))
            else:
                if self.board[row + 1][col] == "--":
                    moves.append(Move((row, col), (row + 1, col), self.board))
                    if row == 1 and self.board[row + 2][col] == "--":
                        moves.append(Move((row, col), (row + 2, col), self.board))

                # Captures to the left
                if col - 1 >= 0 and self.board[row + 1][col - 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col - 1), self.board))
                elif col - 1 >= 0 and (row + 1, col - 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + 1, col - 1),
                                self.board, is_enpassant=True))

                # Captures to the right
                if col + 1 <= 7 and self.board[row + 1][col + 1][0] == "w":
                    moves.append(Move((row, col), (row + 1, col + 1), self.board))
                elif col + 1 <= 7 and (row + 1, col + 1) == self.enpassant_possible:
                    moves.append(Move((row, col), (row + 1, col + 1),
                                self.board, is_enpassant=True))
            return moves
