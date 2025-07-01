import math

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board):
    lines = (
        board + 
        [[board[i][j] for i in range(3)] for j in range(3)] + 
        [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    )
    for line in lines:
        if line == ["X"] * 3:
            return "X"
        if line == ["O"] * 3:
            return "O"
    return None

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def minimax(board, depth, is_maximizing, alpha, beta):
    winner = check_winner(board)
    if winner == "O":
        return 1
    if winner == "X":
        return -1
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        return max_eval
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        return min_eval
        return min_eval

def best_move(board):
    best_val = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = " "
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print("You are X. AI is O.")
    print_board(board)

    while True:
        while True:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter col (0-2): "))
                if board[row][col] == " ":
                    board[row][col] = "X"
                    break
                else:
                    print("Cell is not empty.")
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")

        print_board(board)
        if check_winner(board):
            print(f"{check_winner(board)} wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

        print("AI is making a move...")
        i, j = best_move(board)
        board[i][j] = "O"
        print_board(board)

        if check_winner(board):
            print(f"{check_winner(board)} wins!")
            break
        if is_full(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()