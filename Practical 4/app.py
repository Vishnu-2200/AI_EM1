
from flask import Flask, render_template, request
import math

app = Flask(__name__)

EMPTY = " "
HUMAN = "X"
AI = "O"

WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]


def winner(board):
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] == board[b] == board[c] and board[a] != EMPTY:
            return board[a]
    return None


def minimax(board, depth, is_max, alpha, beta):
    result = winner(board)

    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if EMPTY not in board:
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = AI
                best = max(best, minimax(board, depth + 1, False, alpha, beta))
                board[i] = EMPTY
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best

    best = math.inf
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = HUMAN
            best = min(best, minimax(board, depth + 1, True, alpha, beta))
            board[i] = EMPTY
            beta = min(beta, best)
            if beta <= alpha:
                break
    return best


def best_move(board):
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, 0, False, -math.inf, math.inf)
            board[i] = EMPTY

            if score > best_score:
                best_score = score
                move = i

    return move


@app.route("/", methods=["GET", "POST"])
def index():
    board = [EMPTY] * 9
    message = "Your turn! You are X."

    if request.method == "POST":
        try:
            board = request.form.getlist("board")
            if len(board) != 9 or any(x not in ["X", "O", " "] for x in board):
                raise ValueError()

            move = int(request.form.get("move", -1))

            if winner(board) or EMPTY not in board:
                message = "Game over! Please reset."
            elif 0 <= move < 9 and board[move] == EMPTY:
                board[move] = HUMAN

                if winner(board):
                    message = "You win!"
                elif EMPTY not in board:
                    message = "It's a draw!"
                else:
                    ai_move = best_move(board)
                    if ai_move is not None:
                        board[ai_move] = AI

                    if winner(board):
                        message = "AI wins!"
                    elif EMPTY not in board:
                        message = "It's a draw!"
                    else:
                        message = "Your turn! You are X."
            else:
                message = "Invalid move!"

        except (ValueError, TypeError):
            board = [EMPTY] * 9
            message = "Invalid game state. Please reset."

    return render_template("index.html", board=board, message=message)


if __name__ == "__main__":
    app.run(debug=True)
