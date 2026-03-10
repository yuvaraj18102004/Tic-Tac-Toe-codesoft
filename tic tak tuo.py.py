
import numpy as np
import IPython.display as display
from matplotlib import pyplot as plt
import io
import base64

ys = 200 + np.random.randn(100)
x = [x for x in range(len(ys))]

fig = plt.figure(figsize=(4, 3), facecolor='w')
plt.plot(x, ys, '-')
plt.fill_between(x, ys, 195, where=(ys > 195), facecolor='g', alpha=0.6)
plt.title("Sample Visualization", fontsize=10)

data = io.BytesIO()
plt.savefig(data)
image = F"data:image/png;base64,{base64.b64encode(data.getvalue()).decode()}"
alt = "Sample Visualization"
display.display(display.Markdown(F"""![{alt}]({image})"""))
plt.close(fig)


import math

# Constants
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

# Create board
def create_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]

# Print board
def print_board(board):
    print("\n")
    for row in board:
        print("|".join(row))
        print("-" * 5)

# Check for winner
def check_winner(board):
    # Rows, columns, diagonals
    lines = (
        board +
        [[board[r][c] for r in range(3)] for c in range(3)] +
        [[board[i][i] for i in range(3)]] +
        [[board[i][2 - i] for i in range(3)]]
    )
    for line in lines:
        if line.count(line[0]) == 3 and line[0] != EMPTY:
            return line[0]
    return None

# Check if board is full
def is_full(board):
    return all(cell != EMPTY for row in board for cell in row)

# Evaluate board: +1 = AI win, -1 = Human win, 0 = draw
def evaluate(board):
    winner = check_winner(board)
    if winner == AI:
        return 1
    elif winner == HUMAN:
        return -1
    else:
        return 0

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, is_maximizing):
    winner = check_winner(board)
    if winner or is_full(board):
        return evaluate(board)

    if is_maximizing:
        max_eval = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = AI
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[r][c] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = HUMAN
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[r][c] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Get best move for AI
def get_best_move(board):
    best_score = -math.inf
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = AI
                score = minimax(board, 0, -math.inf, math.inf, False)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (r, c)
    return move

# Human move
def human_move(board):
    while True:
        try:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
            if board[row][col] == EMPTY:
                return row, col
            else:
                print("Cell already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Enter numbers between 0 and 2.")

# Game loop
def play_game():
    board = create_board()
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)
    turn = input("Do you want to be X or O? ").upper()
    global HUMAN, AI
    if turn == 'O':
        HUMAN, AI = AI, HUMAN

    current_player = 'X'

    while True:
        if current_player == HUMAN:
            print("Your turn.")
            r, c = human_move(board)
            board[r][c] = HUMAN
        else:
            print("AI's turn.")
            r, c = get_best_move(board)
            board[r][c] = AI

        print_board(board)
        winner = check_winner(board)

        if winner:
            print(f"{winner} wins!")
            break
        elif is_full(board):
            print("It's a draw!")
            break

        current_player = AI if current_player == HUMAN else HUMAN

# Start the game
if __name__ == "__main__":
    play_game()
