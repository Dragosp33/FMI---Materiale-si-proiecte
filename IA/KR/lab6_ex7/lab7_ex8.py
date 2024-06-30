import numpy as np

ROWS = 6
COLS = 7
PLAYER = 1
AI = 2
EMPTY = 0

# Create an empty game board
def create_board():
    board = np.zeros((ROWS, COLS))
    return board

# Check if a move is valid
def is_valid_move(board, col):
    return board[ROWS - 1][col] == 0

# Make a move on the board
def make_move(board, col, player):
    for row in range(ROWS):
        if board[row][col] == 0:
            board[row][col] = player
            break

# Check if the game is over
def is_game_over(board):
    # Check for a win in rows
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (
                board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != 0
            ):
                return True, board[row][col]

    # Check for a win in columns
    for col in range(COLS):
        for row in range(ROWS - 3):
            if (
                board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != 0
            ):
                return True, board[row][col]

    # Check for a win in positive slope diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (
                board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != 0
            ):
                return True, board[row][col]

    # Check for a win in negative slope diagonals
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if (
                board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] != 0
            ):
                return True, board[row][col]

    # Check for a draw
    if np.all(board != 0):
        return True, 0

    return False, None

# Evaluate the board state
def evaluate_board(board):
    score = 0

    # Evaluate horizontal windows
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row, col:col + 4]
            score += evaluate_window(window)

    # Evaluate vertical windows
    for row in range(ROWS - 3):
        for col in range(COLS):
            window = board[row:row + 4, col]
            score += evaluate_window(window)

    # Evaluate diagonal windows (positive slope)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window)

    # Evaluate diagonal windows (negative slope)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window)

    return score

# Evaluate a window of 4 cells
def evaluate_window(window):
    score = 0
    player_count = np.count_nonzero(window == PLAYER)
    ai_count = np.count_nonzero(window == AI)
    empty_count = np.count_nonzero(window == EMPTY)

    # Score the window based on the number of player and AI pieces
    if player_count == 4:
        score += 100
    elif player_count == 3 and empty_count == 1:
        score += 5
    elif player_count == 2 and empty_count == 2:
        score += 2

    if ai_count == 3 and empty_count == 1:
        score -= 4

    return score

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    game_over, winner = is_game_over(board)

    if depth == 0 or game_over:
        if game_over:
            if winner == AI:
                return None, 1000000000000
            elif winner == PLAYER:
                return None, -1000000000000
            else:
                return None, 0
        else:
            return None, evaluate_board(board)

    if maximizing_player:
        max_eval = -float('inf')
        best_col = None
        valid_moves = get_valid_moves(board)
        for col in valid_moves:
            temp_board = board.copy()
            make_move(temp_board, col, AI)
            _, eval = minimax(temp_board, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_col = col
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return best_col, max_eval

    else:
        min_eval = float('inf')
        best_col = None
        valid_moves = get_valid_moves(board)
        for col in valid_moves:
            temp_board = board.copy()
            make_move(temp_board, col, PLAYER)
            _, eval = minimax(temp_board, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_col = col
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return best_col, min_eval

# Get a list of valid moves for the current board state
def get_valid_moves(board):
    valid_moves = []
    for col in range(COLS):
        if is_valid_move(board, col):
            valid_moves.append(col)
    return valid_moves

# Print the game board
def print_board(board):
    print(np.flip(board, 0))

# Main game loop
def play_game():
    board = create_board()
    game_over = False
    current_player = PLAYER

    while not game_over:
        print_board(board)

        if current_player == PLAYER:
            col = int(input("Your turn (0-6): "))
            if is_valid_move(board, col):
                make_move(board, col, current_player)
                game_over, winner = is_game_over(board)
                if game_over:
                    if winner == PLAYER:
                        print("Congratulations! You win!")
                    elif winner == AI:
                        print("AI wins!")
                    else:
                        print("It's a draw!")
                else:
                    current_player = AI
            else:
                print("Invalid move. Please try again.")

        else:
            print("AI is thinking...")
            col, _ = minimax(board, 5, -float('inf'), float('inf'), True)
            make_move(board, col, AI)
            game_over, winner = is_game_over(board)
            if game_over:
                if winner == PLAYER:
                    print("Congratulations! You win!")
                elif winner == AI:
                    print_board(board)
                    print("AI wins!")
                else:
                    print("It's a draw!")
            else:
                current_player = PLAYER

play_game()