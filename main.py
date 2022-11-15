from random import choice


board = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]


def print_board(board):
    colcount = 0
    rowcount = 0
    div = "  ---+---+---"
    print("   A   B   C")   # aggiunge header delle colonne
    for row_id, row in enumerate(board):
        print(f"{row_id+1}  ", end="")  # aggiunge numero riga e spazio prima del primo carattere
        for col in row:
            if colcount < 2:
                print(f"{col}", end=" | ")
                colcount = colcount + 1
            else:
                print(col, end=" ")
        colcount = 0
        print(" ")  # aggiunge spazio dopo l'ultimo carattere
        if rowcount < 2:
            print(div)
            rowcount = rowcount + 1
    print("\n")


def is_board_full(board):
    for row in board:
        for col in row:
            if "#" in col:
                return False
    return True


def update_board(board, row, col, player):
    if board[row][col] == "#":
        board[row][col] = player
        return True
    else:
        return False


def convert_coord(usrcoord):
    if usrcoord[0].isdigit():
        row = int(usrcoord[0]) - 1
        col = usrcoord[1].upper()
    else:
        row = int(usrcoord[1]) - 1
        col = usrcoord[0].upper()
    if col == "A":
        col = 0
    elif col == "B":
        col = 1
    elif col == "C":
        col = 2
    return row, col


def check_coord(row, col):
    if row > 2 or col > 2:
        return False
    else:
        return True


def player_move(board, usrrow, usrcol, player):
    if check_coord(usrrow, usrcol):
        if update_board(board, usrrow, usrcol, player):
            update_board(board, usrrow, usrcol, player)
            print_board(board)
    else:
        print("Coordinate invalide")


def random_player():
    return choice(["X", "O"])


def check_win(player):
    win = None
    n = len(board)
    for i in range(n):
        win = True
        for j in range(n):
            if board[i][j] != player:
                win = False
                break
        if win:
            return win
    for i in range(n):
        win = True
        for j in range(n):
            if board[j][i] != player:
                win = False
                break
        if win:
            return win
    win = True
    for i in range(n):
        if board[i][i] != player:
            win = False
            break
    if win:
        return win
    win = True
    for i in range(n):
        if board[i][n - 1 - i] != player:
            win = False
            break
    if win:
        return win
    return False


def main():
    print("Tic Tac Toe\n\n")
    player = random_player()
    while not is_board_full(board):
        print(f"Turno del giocatore {player}\n")
        print_board(board)
        coord_input = input("Inserisci le coordinate: ")
        if len(coord_input) == 2:
            row_input, col_input = convert_coord(coord_input)
            if check_coord(row_input, col_input):
                if update_board(board, row_input, col_input, player):
                    print_board(board)
                    if player == "X":
                        player = "O"
                    else:
                        player = "X"
                else:
                    print("Coordinate non valide, cassella già occupata")
            else:
                print("Coordinate invalide")
            print("--------------")
            if check_win(player):
                print("")
                print(f"Vince il giocatore {player}")
                break
            print("Coordinate non valide")


main()

