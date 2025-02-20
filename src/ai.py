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
DEPTH = 2

'''
Get a random move from the list of valid moves
'''


def get_random_move(valid_moves):
    return random.choice(valid_moves)


'''
def get_best_move(game_state, valid_moves):
    turn_multiplier = 1 if game_state.white_to_move else -1
    best_move = None
    random.shuffle(valid_moves)
    opponent_minmax_score = CHECKMATE
    for move in valid_moves:
        game_state.make_move(move)
        opponent_moves = game_state.get_valid_moves()
        if game_state.checkmate:
            opponent_maxscore = -CHECKMATE
        elif game_state.stalemate:
            opponent_maxscore = STALEMATE 
        else:
            opponent_maxscore = -CHECKMATE
            for opponent_move in opponent_moves:
                game_state.make_move(opponent_move)
                game_state.get_valid_moves()
                if game_state.checkmate:
                    score = CHECKMATE
                elif game_state.stalemate:
                    score = STALEMATE
                else:
                    score = -turn_multiplier * score_material(game_state.board)
                if score > opponent_minmax_score:
                    opponent_minmax_score = score
                game_state.undo_move()
        if opponent_maxscore < opponent_minmax_score:
            opponent_minmax_score = opponent_maxscore
            best_move = move
        game_state.undo_move()

    return best_move
'''
'''
Get the best move from the list of valid moves
'''


def get_best_move(game_state, valid_moves):
    global next_move
    next_move = None
    get_minmax_move(game_state, valid_moves, DEPTH, game_state.white_to_move)    
    return next_move


'''
Get best move using minmax recursively
'''


def get_minmax_move(game_state, valid_moves, depth, white_to_move):
    if depth == 0:
        return score_material(game_state)
    
    if white_to_move:
        max_score = -CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            
            next_move = game_state.get_valid_moves()
            score = get_minmax_move(game_state, next_move, depth - 1, False)
            
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    next_move == move
            
            game_state.undo_move()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            game_state.make_move(move)
            
            next_move = game_state.get_valid_moves()
            score = get_minmax_move(game_state, next_move, depth - 1, True)
            
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    next_move == move
            
            game_state.undo_move()
        return min_score


'''
Score the board based on the current material

Positive is good for white, and negative is good for black
'''


def score_material(game_state):
    score = 0
    
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif game_state.stalemate:
        return STALEMATE
    
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

    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
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
