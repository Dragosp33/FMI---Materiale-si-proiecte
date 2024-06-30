def create_board(n):
    return [['#' for _ in range(n)] for _ in range(n)]

def print_board(board):
    for row in board:
        print(' '.join(row))
    print()

def get_move(player, board):
    while True:
        try:
            row = int(input(f"{player} - Enter the row number: "))
            col = int(input(f"{player} - Enter the column number: "))
            if board[row][col] == '#':
                return row, col
            else:
                print("Invalid move! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Try again.")

def is_goal_state(board, k, player):
    n = len(board)
    # Check rows
    for row in range(n):
        count = 0
        for col in range(n):
            if board[row][col] == player:
                count += 1
                if count == k:
                    return True
            else:
                count = 0

    # Check columns
    for col in range(n):
        count = 0
        for row in range(n):
            if board[row][col] == player:
                count += 1
                if count == k:
                    return True
            else:
                count = 0

    # Check diagonals
    for i in range(n - k + 1):
        for j in range(n - k + 1):
            count = 0
            for x in range(k):
                if board[i + x][j + x] == player:
                    count += 1
                    if count == k:
                        return True
                else:
                    count = 0

            count = 0
            for x in range(k):
                if board[i + x][j + k - 1 - x] == player:
                    count += 1
                    if count == k:
                        return True
                else:
                    count = 0

    return False

def estimate_score(board, k, player):
    n = len(board)
    score = 0

    # Check rows
    for row in range(n):
        count = 0
        empty = 0
        for col in range(n):
            if board[row][col] == player:
                count += 1
            elif board[row][col] == '#':
                empty += 1
            else:
                count = 0
                empty = 0

            if count + empty == k:
                score += 10 ** count
                if empty == 1:
                    score += 1

    # Check columns
    for col in range(n):
        count = 0
        empty = 0
        for row in range(n):
            if board[row][col] == player:
                count += 1
            elif board[row][col] == '#':
                empty += 1
            else:
                count = 0
                empty = 0

            if count + empty == k:
                score += 10 ** count
                if empty == 1:
                    score += 1

    # Check diagonals
    for i in range(n - k + 1):
        for j in range(n - k + 1):
            count = 0
            empty = 0
            for x in range(k):
                if board[i + x][j + x] == player:
                    count += 1
                elif board[i + x][j + x] == '#':
                    empty += 1
                else:
                    count = 0
                    empty = 0

                if count + empty == k:
                    score += 10 ** count
                    if empty == 1:
                        score += 1

            count = 0
            empty = 0
            for x in range(k):
                if board[i + x][j + k - 1 - x] == player:
                    count += 1
                elif board[i + x][j + k - 1 - x] == '#':
                    empty += 1
                else:
                    count = 0
                    empty = 0

                if count + empty == k:
                    score += 10 ** count
                    if empty == 1:
                        score += 1

    return score

def play_game():
    n = int(input("Enter the size of the game board (3-5): "))
    if n < 3 or n > 5:
        print("Invalid size. The program will exit.")
        return

    variant = input("Select the game variant (a, b, or c): ")
    if variant not in ['a', 'b', 'c']:
        print("Invalid variant. The program will exit.")
        return

    k = n if variant == 'a' else int(input(f"Enter the size of the winning configuration (3-{n}): "))

    players = ['x', '0']
    board = create_board(n)
    player_index = 0

    while True:
        print_board(board)
        player = players[player_index]
        move = get_move(player, board)
        board[move[0]][move[1]] = player

        if is_goal_state(board, k, player):
            print(f"{player} wins!")
            break
        elif all(board[i][j] != '#' for i in range(n) for j in range(n)):
            print("It's a draw!")
            break

        player_index = 1 - player_index

play_game()