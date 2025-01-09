"""
Logic for the chess engine
"""
import numpy as np


class GameState:
    def __init__(self):
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ])
        self.white_to_move = True
        self.moveLog = []

    # Make move using the move object.
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.moveLog.append(move)
        self.white_to_move = not self.white_to_move

    # Undo a move from the move log.
    def undo_move(self):
        if len(self.moveLog) != 0:  # Log should be non-empty to undo
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

    # Generate every valid moves
    def get_valid_moves(self):
        return self.get_all_possible_moves()

    # Generate every possible moves for every piece
    def get_all_possible_moves(self):
        moves = []
        for rows in range(len(self.board)):
            for cols in range(len(self.board[rows])):
                turn = self.board[rows][cols][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[rows][cols][1]
                    if piece == "P":
                        self.get_pawn_moves(rows, cols, moves)
                    elif piece == "R":
                        self.get_rook_moves(rows, cols, moves)
                    elif piece == "N":
                        self.get_knight_moves(rows, cols, moves)
                    elif piece == "B":
                        self.get_bishop_moves(rows, cols, moves)
                    elif piece == "Q":
                        self.get_queen_moves(rows, cols, moves)
                    else:
                        self.get_king_moves(rows, cols, moves)
        return moves

    # Generate all moves possible for the given pawn at the row and column
    def get_pawn_moves(self, rows, cols, moves):
        if self.white_to_move:
            if self.board[rows - 1][cols] == "--":  # One square pawn advance
                moves.append(Move((rows, cols), (rows - 1, cols), self.board))
                if rows == 6 and self.board[rows - 2][cols] == "--":  # Two square pawn advance
                    moves.append(Move((rows, cols), (rows - 2, cols), self.board))

            # Captures to the left
            if cols - 1 >= 0 and self.board[rows - 1][cols - 1][0] == "b":  # Enemy piece on the diagonal
                moves.append(Move((rows, cols), (rows - 1, cols - 1), self.board))

            # Captures to the right
            if cols + 1 <= 7 and self.board[rows - 1][cols + 1][0] == "b":
                moves.append(Move((rows, cols), (rows - 1, cols + 1), self.board))
        else:
            if self.board[rows + 1][cols] == "--":
                moves.append(Move((rows, cols), (rows + 1, cols), self.board))
                if rows == 1 and self.board[rows + 2][cols] == "--":
                    moves.append(Move((rows, cols), (rows + 2, cols), self.board))

            if cols - 1 >= 0 and self.board[rows + 1][cols - 1][0] == "w":
                moves.append(Move((rows, cols), (rows + 1, cols - 1), self.board))

            if cols + 1 <= 7 and self.board[rows + 1][cols + 1][0] == "w":
                moves.append(Move((rows, cols), (rows + 1, cols + 1), self.board))

    # Generate all moves possible for the given rook at the row and column
    def get_rook_moves(self, rows, cols, moves):
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy = "b" if self.white_to_move else "w"

        for d in direction:
            for i in range(1, 8):
                end_row = rows + d[0] * i
                end_col = cols + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((rows, cols), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((rows, cols), (end_row, end_col), self.board))
                        break  # We can't jump the enemy piece
                    else:  # Friendly piece
                        break
                else:  # Out of board
                    break

    # Generate all moves possible for the given knight at the row and column
    def get_knight_moves(self, rows, cols, moves):
        knight_moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally = "w" if self.white_to_move else "b"
        for move in knight_moves:
            end_row = rows + move[0]
            end_col = cols + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally:
                    moves.append(Move((rows, cols), (end_row, end_col), self.board))

    # Generate all moves possible for the given bishop at the row and column
    def get_bishop_moves(self, rows, cols, moves):
        direction = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy = "b" if self.white_to_move else "w"

        for d in direction:
            for i in range(1, 8):
                end_row = rows + d[0] * i
                end_col = cols + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move((rows, cols), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy:
                        moves.append(Move((rows, cols), (end_row, end_col), self.board))
                        break  # We can't jump the enemy piece
                    else:  # Friendly piece
                        break
                else:  # Out of board
                    break

    # Generate all moves possible for the given queen at the row and column
    def get_queen_moves(self, rows, cols, moves):
        self.get_rook_moves(rows, cols, moves)
        self.get_bishop_moves(rows, cols, moves)

    # Generate all moves possible for the given king at the row and column
    def get_king_moves(self, rows, cols, moves):
        king_moves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally = "w" if self.white_to_move else "b"
        for move in king_moves:
            end_row = rows + move[0]
            end_col = cols + move[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally:
                    moves.append(Move((rows, cols), (end_row, end_col), self.board))


class Move:
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.move_id = 1000 * self.start_row + 100 * self.start_col + 10 * self.end_row + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
