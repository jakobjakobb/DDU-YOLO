from game_computer import easy_move, medium_move, hard_move
from game_logic import check_winner, get_available_moves, display_board
board = ["" for _ in range(9)]

def reset_board():
    board[:] = ["" for _ in range(9)]


def make_move(player, move_index, cheating_allowed=False):
    if not 0 <= move_index <= 8:
        raise ValueError("Move is out of bounds!")
    if (not cheating_allowed) and board[move_index] != "":
        raise ValueError("You can't move on top of another piece!")

    board[move_index] = player

    

def computer_move(difficulty="easy"):
    match difficulty.lower():
        case "easy": return easy_move(board)
        case "medium": return medium_move(board)
        case "hard": return hard_move(board)
        case _: raise ValueError("Invalid difficulty!")

    



    
def _test():
    while True:
        reset_board()

        difficulty = input("> Choose a difficulty (Easy|Medium|Hard): ").lower()
        if not difficulty in ["easy","medium","hard"]:
            print("Invalid difficulty!")
            continue

        while True:
            display_board(board)
            choice = input("> Choose a position (1-9): ")

            try:
                make_move("X", (int(choice)-1))
            except ValueError as e:
                print(e)
                continue

            if check_winner(board, "X"): 
                display_board(board)
                print("You won!")
                break

            if not get_available_moves(board):
                display_board(board)
                print("It's a tie!")
                break
            
            make_move("O", computer_move(difficulty))

            if check_winner(board, "O"):
                display_board(board)
                print("The computer won!")
                break




if __name__ == "__main__":
    _test()