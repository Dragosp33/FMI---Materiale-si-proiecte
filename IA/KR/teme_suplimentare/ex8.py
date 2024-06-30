import numpy as np

ROWS = 7
COLS = 7
PLAYER = 1
AI = 2
EMPTY = 0


def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col].any() == EMPTY:
            return r

# Create an empty game board
def create_board():
    board = np.zeros((ROWS, COLS))
    return board



# move valid. board[0][col] == 0, pt a incepe de sus in jos
def is_valid_move(board, col):
    return board[0][col] == 0

# Make a move on the board
def make_move(board, col, player):
    row = get_next_open_row(board, col)
    board[row][col] = player


# is_goal:
def is_game_over(board):
    # vedem daca a castigat cineva
    for row in range(ROWS):
        for col in range(COLS - 3):
            if (
                board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != 0
            ):
                return True, board[row][col]


    for col in range(COLS):
        for row in range(ROWS - 3):
            if (
                board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != 0
            ):
                return True, board[row][col]

    # diagonala:
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if (
                board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != 0
            ):
                return True, board[row][col]

    # diagonala stanga:
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


    for row in range(ROWS - 3):
        for col in range(COLS):
            window = board[row:row + 4, col]
            score += evaluate_window(window)

    # evalueaza diagonala:
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window)

    # evalueaza diagonala stanga:
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

    # Sscor 100 - a castigat AI
    if ai_count == 4:
        score += 100
    elif ai_count == 3 and empty_count == 1:
        score += 5
    elif ai_count == 2 and empty_count == 2:
        score += 2

    if player_count == 3 and empty_count == 1:
        score -= 4

    return score

# Minimax cu alpha-beta pt a elimina crearea de noduri care oricum nu ar modifica rezultatul
def minimax(board, depth, alpha, beta, maximizing_player):
    game_over, winner = is_game_over(board)
    # se returneaza None pt ca nu mai avem coloana de pus, deja s-a terminat
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
    # minmax scris altfel, daca maximize_player, adica daca e randul calculatorului, max_eval = -inf
    # pt a calcula maximul si a-l folosi
    # analog, pt jucator, minimul o sa fie + infinit iar mai apoi va fi inlocuit de cea mai mica valoare
    if maximizing_player:
        max_eval = -float('inf')
        best_col = None
        valid_moves = get_valid_moves(board)
        for col in valid_moves:
            temp_board = board.copy()
            make_move(temp_board, col, AI)
            _, eval = minimax(temp_board, depth - 1, alpha, beta, False)
            #apoi minmax cu False la maximize
            if eval > max_eval:
                max_eval = eval
                best_col = col
            alpha = max(alpha, eval)
            #alpha devine cel mai mare scor, pt AI
            if alpha >= beta:
                # daca alpha >= beta, e clar ca nu vom gasi alt scor mai mic
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
            # luam minimul pt jucator
            # daca alpha mai mare decat beta, clar nu gasim un scor mai bun, deci nu mai are rost sa calculam toate
            # posibilitatile
            if alpha >= beta:
                break
        return best_col, min_eval

# lista de miscari valide:
def get_valid_moves(board):
    valid_moves = []
    for col in range(COLS):
        if is_valid_move(board, col):
            valid_moves.append(col)
    return valid_moves

# Print the game board
def print_board(board):
    for r in range(ROWS - 1, -1, -1):
        row_str = "| "
        for c in range(COLS):
            if board[r][c] == PLAYER:
                row_str += "P "
            elif board[r][c] == AI:
                row_str += "A "
            else:
                row_str += "  "
            row_str += "| "
        print(row_str)

    print("-----------------------------")
    print("| 0 | 1 | 2 | 3 | 4 | 5 | 6 |")
    print("-----------------------------")


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
                        print_board(board)
                    elif winner == AI:
                        print("AI wins!")

                    else:
                        print("It's a draw!")
                        print_board(board)
                else:
                    current_player = AI
            else:
                print("Invalid move. Please try again.")

        else:
            print("AI is thinking...")
            col, _ = minimax(board, 5, -float('inf'), float('inf'), True)
            # alpha va fi -inf; beta va fi infinit;
            make_move(board, col, AI)
            game_over, winner = is_game_over(board)
            if game_over:
                if winner == PLAYER:
                    print("Congratulations! You win!")

                elif winner == AI:
                    print("AI wins!")
                    print_board(board)
                else:
                    print("It's a draw!")
            else:
                current_player = PLAYER

play_game()