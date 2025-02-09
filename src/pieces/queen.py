'''
class Queen gets the moves of the queen piece on the board
'''

from pieces.piece import Piece
from pieces.rook import Rook
from pieces.bishop import Bishop

class Queen(Piece):
    def get_moves(self, row, col):
        moves = []
        rook = Rook(self.board, self.white_to_move)
        bishop = Bishop(self.board, self.white_to_move)
        moves.extend(rook.get_moves(row, col))
        moves.extend(bishop.get_moves(row, col))
        return moves