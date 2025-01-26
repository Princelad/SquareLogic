"""
Logic for the chess engine.
"""

import numpy as np


class GameState:
    """
    Represents the current state of a chess game.
    """

    def __init__(self):
        """
        Initializes the chessboard, turn indicator, and move log.
        """
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
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def make_move(self, move):
        """
        Executes a move on the board and updates game state.
        """
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)

        # Update king's location
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        self.white_to_move = not self.white_to_move

    def undo_move(self):
        """
        Reverts the last move from the move log.
        """
        if self.move_log:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured

            # Update king's location
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_col)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_col)

            self.white_to_move = not self.white_to_move

    def get_valid_moves(self):
        """
        Returns all valid moves, filtering out moves that leave the king in check.
        """
        moves = self.get_all_possible_moves()
        valid_moves = []

        for move in moves:
            self.make_move(move)
            self.white_to_move = not self.white_to_move  # Simulate opponent's turn
            if not self.in_check():
                valid_moves.append(move)
            self.white_to_move = not self.white_to_move  # Undo simulation
            self.undo_move()

        # Either stalemate or checkmate
        if len(valid_moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.stalemate = False
            self.checkmate = False

        return valid_moves

    def in_check(self):
        """
        Checks if the current player's king is in check.
        """
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, row, col):
        """
        Checks if the given square is under attack by the opponent.
        """
        self.white_to_move = not self.white_to_move
        opp_moves = self.get_all_possible_moves()
        self.white_to_move = not self.white_to_move

        return any(move.end_row == row and move.end_col == col for move in opp_moves)

    def get_all_possible_moves(self):
        """
        Generates all possible moves for the current player.
        """
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece_type = self.board[row][col][1]
                    self.get_piece_moves(piece_type, row, col, moves)
        return moves

    def get_piece_moves(self, piece_type, row, col, moves):
        """
        Generates moves for a specific piece based on its type.
        """
        if piece_type == "P":
            self.get_pawn_moves(row, col, moves)
        elif piece_type == "R":
            self.get_rook_moves(row, col, moves)
        elif piece_type == "N":
            self.get_knight_moves(row, col, moves)
        elif piece_type == "B":
            self.get_bishop_moves(row, col, moves)
        elif piece_type == "Q":
            self.get_queen_moves(row, col, moves)
        elif piece_type == "K":
            self.get_king_moves(row, col, moves)

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
    """
    Represents a chess move with start and end positions, and metadata.
    """
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
