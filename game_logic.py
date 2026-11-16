def check_winner(b, player):
    win_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    
    return any(all(b[i] == player for i in combination) for combination in win_combinations)

def get_available_moves(b):
    return [i for i, cell in enumerate(b) if cell == ""]

def display_board(b):

    d = [(i.replace("", "  ") if i == "" else f" {i}" if len(i) == 1 else i) for i in b]

    print(f"""

 {d[0]} │ {d[1]} │ {d[2]}
────┼────┼────
 {d[3]} │ {d[4]} │ {d[5]}
────┼────┼────
 {d[6]} │ {d[7]} │ {d[8]}

""")
    
def get_player_turn(b):
    return "X" if b.count("X") <= b.count("O") else "O"