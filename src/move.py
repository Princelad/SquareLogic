class Move:
    """
    Represents a chess move with start and end positions, and metadata.
    """
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant=False, is_castle=False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # Pawn Promotion
        self.is_pawn_promotion = ((self.piece_moved == "wP" and self.end_row == 0) or (
                self.piece_moved == "bP" and self.end_row == 7))

        # Enpassant
        self.is_enpassant = is_enpassant
        if is_enpassant:
            self.piece_captured = "wP" if self.piece_moved == "wP" else "bP"

        # Castle move
        self.is_castle = is_castle

        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        return isinstance(other, Move) and self.move_id == other.move_id

    def get_chess_notation(self):
        """
        Converts the move to standard chess notation.
        """
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        """
        Converts a row and column to chess notation (e.g., 'e2').
        """
        return self.cols_to_files[col] + self.rows_to_ranks[row]