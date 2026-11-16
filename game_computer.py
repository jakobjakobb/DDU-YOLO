from random import choice
from game_logic import check_winner, get_available_moves, get_player_turn

def easy_move(b):
    return choice(get_available_moves(b))

def medium_move(b):
    available = get_available_moves(b)
    comp_icon = get_player_turn(b)
    human_icon = "X" if comp_icon == "O" else "O"
    
    for move in available:
        b[move] = comp_icon
        if check_winner(b, comp_icon):
            b[move] = ""
            return move
        b[move] = ""
        
    for move in available:
        b[move] = human_icon
        if check_winner(b, human_icon):
            b[move] = ""
            return move
        b[move] = ""
        
    if 4 in available:
        return 4
        
    corners = [i for i in [0, 2, 6, 8] if i in available]
    if corners:
        return choice(corners)
        
    return choice(available)

def minimax(b, is_maximizing, comp_icon, human_icon, depth=0):
    if check_winner(b, comp_icon):
        return 10 - depth
    if check_winner(b, human_icon):
        return -10 + depth
        
    available = get_available_moves(b)
    if not available:
        return 0

    if is_maximizing:
        best_score = float("-inf")
        for move in available:
            b[move] = comp_icon
            score = minimax(b, False, comp_icon, human_icon, depth + 1)
            b[move] = ""
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for move in available:
            b[move] = human_icon
            score = minimax(b, True, comp_icon, human_icon, depth + 1)
            b[move] = ""
            best_score = min(score, best_score)
        return best_score


def hard_move(b):
    available = get_available_moves(b)
    comp_icon = get_player_turn(b)
    human_icon = "X" if comp_icon == "O" else "O"
    
    best_score = float("-inf")
    best_moves = []
    
    for move in available:
        b[move] = comp_icon
        score = minimax(b, False, comp_icon, human_icon)
        b[move] = ""
        
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)
            
    return choice(best_moves)
