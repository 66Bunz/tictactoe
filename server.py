
import socket, sys, time
from random import choice


host = "0.0.0.0"
port = 5987

board = [['#', '#', '#'], ['#', '#', '#'], ['#', '#', '#']]

connections = []
addresses = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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


def print_board(board):
    colcount = 0
    rowcount = 0
    div = "  ---+---+---"
    print("   A   B   C")
    for row_id, row in enumerate(board):
        print(f"{row_id+1}  ", end="")
        for col in row:
            if colcount < 2:
                print(f"{col}", end=" | ")
                colcount = colcount + 1
            else:
                print(col, end=" ")
        colcount = 0
        print(" ")
        if rowcount < 2:
            print(div)
            rowcount = rowcount + 1
    print("")


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


def get_input(player):
    try:
        if player == "X":
            conn = connections[0]
            conn.send(f"board{str(board)}".encode())
            conn.send("Input".encode())
            coord_input = conn.recv(2048 * 10).decode()
            return coord_input
        else:
            conn = connections[1]
            conn.send(f"board{str(board)}".encode())
            conn.send("Input".encode())
            coord_input = conn.recv(2048 * 10).decode()
            return coord_input
    except:
        print("Unexpected error:", sys.exc_info()[0])


def send_common_message(message):
    if isinstance(message, str):
        for conn in connections:
            conn.send(message.encode())
            time.sleep(0.15)


def random_player():
    return choice(["X", "O"])


def start_game():
    player = random_player()
    send_common_message("Start")
    while not is_board_full(board):
        print(f"Turno del giocatore {player}\n")
        send_common_message(f"{player}")
        print_board(board)
        if player == "X":
            coord_input = get_input(player)
            player = "O"
        else:
            coord_input = get_input(player)
            player = "X"

        row_input, col_input = convert_coord(coord_input)
        update_board(board, row_input, col_input, player)

        print_board(board)
        send_common_message(f"board{str(board)}")

        print("--------------")
        send_common_message("Divider")
        if check_win(player):
            print(f"\nVince il giocatore {player}")
            send_common_message(f"Vince {player}")
            break
    else:
        print("Pareggio")
        send_common_message("Pareggio")


def accept_players():
    try:
        for i in range(2):
            conn, addr = server.accept()
            print("Connection from: " + str(addr))
            conn.send("Tic Tac Toe".encode())
            connections.append(conn)
            addresses.append(addr)
            if i == 0:
                print(f"1st Player: X [{addr[0]}:{str(addr[1])}]")
                conn.send("IX".encode())
            else:
                print(f"2nd Player: O [{addr[0]}:{str(addr[1])}]")
                conn.send("IO".encode())
            print("")
        print("")
        start_game()
        server.close()
    except socket.error as e:
        print("Server connection error:", e)
    except:
        print("Unexpected error:", sys.exc_info()[0])


def start_server():
    try:
        server.bind((host, port))
        print("Tic Tac Toe server started \nBinding to port", port)
        server.listen(2)
        accept_players()
    except socket.error as e:
        print("Server binding error:", e)


def main():
    start_server()


if __name__ == '__main__':
    main()
