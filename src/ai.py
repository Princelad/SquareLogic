import random

piece_values = {
    "K": 0,
    "Q": 9,
    "R": 5,
    "B": 3,
    "N": 3,
    "P": 1
}
CHECKMATE = 1000
STALEMATE = 0

'''
Get a random move from the list of valid moves
'''


def get_random_move(valid_moves):
    return random.choice(valid_moves)


'''
Get the best move from the list of valid moves
'''


def get_best_move(game_state, valid_moves):
    turn_multiplier = 1 if game_state.white_to_move else -1
    best_move = None
    worst_score = -CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        if game_state.checkmate:
            score = CHECKMATE
        elif game_state.stalemate:
            score = STALEMATE
        else:
            score = turn_multiplier * score_material(game_state.board)
        if score > worst_score:
            worst_score = score
            best_move = move
        game_state.undo_move()

    return best_move


'''
Score the board based on the current material
'''


def score_material(board):
    score = 0
    piece_square_table = {
        "P": [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 5, 5, 5, 5, 5, 5, 5,
            1, 1, 2, 3, 3, 2, 1, 1,
            0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5,
            0, 0, 0, 2, 2, 0, 0, 0,
            0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5,
            0.5, 1, 1, -2, -2, 1, 1, 0.5,
            0, 0, 0, 0, 0, 0, 0, 0
        ],
        "N": [
            -5, -4, -3, -3, -3, -3, -4, -5,
            -4, -2, 0, 0, 0, 0, -2, -4,
            -3, 0, 1, 1.5, 1.5, 1, 0, -3,
            -3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3,
            -3, 0, 1.5, 2, 2, 1.5, 0, -3,
            -3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3,
            -4, -2, 0, 0.5, 0.5, 0, -2, -4,
            -5, -4, -3, -3, -3, -3, -4, -5
        ],
        "B": [
            -2, -1, -1, -1, -1, -1, -1, -2,
            -1, 0, 0, 0, 0, 0, 0, -1,
            -1, 0, 0.5, 1, 1, 0.5, 0, -1,
            -1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1,
            -1, 0, 1, 1, 1, 1, 0, -1,
            -1, 1, 1, 1, 1, 1, 1, -1,
            -1, 0.5, 0, 0, 0, 0, 0.5, -1,
            -2, -1, -1, -1, -1, -1, -1, -2
        ],
        "R": [
            0, 0, 0, 0, 0, 0, 0, 0,
            0.5, 1, 1, 1, 1, 1, 1, 0.5,
            -0.5, 0, 0, 0, 0, 0, 0, -0.5,
            -0.5, 0, 0, 0, 0, 0, 0, -0.5,
            -0.5, 0, 0, 0, 0, 0, 0, -0.5,
            -0.5, 0, 0, 0, 0, 0, 0, -0.5,
            -0.5, 0, 0, 0, 0, 0, 0, -0.5,
            0, 0, 0, 0.5, 0.5, 0, 0, 0
        ],
        "Q": [
            -2, -1, -1, -0.5, -0.5, -1, -1, -2,
            -1, 0, 0, 0, 0, 0, 0, -1,
            -1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1,
            -0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
            0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5,
            -1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1,
            -1, 0, 0.5, 0, 0, 0, 0, -1,
            -2, -1, -1, -0.5, -0.5, -1, -1, -2
        ],
        "K": [
            -3, -4, -4, -5, -5, -4, -4, -3,
            -3, -4, -4, -5, -5, -4, -4, -3,
            -3, -4, -4, -5, -5, -4, -4, -3,
            -3, -4, -4, -5, -5, -4, -4, -3,
            -2, -3, -3, -4, -4, -3, -3, -2,
            -1, -2, -2, -2, -2, -2, -2, -1,
            2, 2, 0, 0, 0, 0, 2, 2,
            2, 3, 1, 0, 0, 1, 3, 2
        ]
    }

    for row in range(len(board)):
        for col in range(len(board[row])):
            piece = board[row][col]
            if piece != "--":
                piece_type = piece[1]
                piece_color = piece[0]
                piece_value = piece_values[piece_type]
                position_value = piece_square_table[piece_type][col * 8 + row]
                if piece_color == "w":
                    score += piece_value + position_value
                elif piece_color == "b":
                    score -= piece_value + position_value
    return score
