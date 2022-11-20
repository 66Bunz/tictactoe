
import socket, time
import sys

host = "localhost"
port = 5987

server = socket.socket()


def print_board(board):
    colcount = 0
    rowcount = 0
    div = "  ---+---+---"
    print("")
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
    print("\n")


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


def start_game():
    title = server.recv(2048 * 10)
    print(title.decode())

    print("")

    welcome = server.recv(2048 * 10)
    if welcome.decode() == "IX":
        player = "X"
        print("Ciao, benvenuto sul server di tris.\nTu sarai il giocatore X\n")
    else:
        player = "O"
        print("Ciao, benvenuto sul server di tris.\nTu sarai il giocatore O\n")

    print("Attendendo un avversario...\n")

    while True:
        recvData = server.recv(2048 * 10)
        recvDataDecode = recvData.decode()

        try:
            if "Input" in recvDataDecode:
                coord_input = input("Inserisci le coordinate: ")
                row, col = convert_coord(coord_input)
                while len(coord_input) != 2 or (len(coord_input) != 2 and (row > 2 or col > 2)) or board[row][col] != "#":
                    print("Coordinate non valide")
                    coord_input = input("Inserisci le coordinate: ")
                    row, col = convert_coord(coord_input)
                else:
                    print("")
                    server.send(coord_input.encode())

            elif recvDataDecode == "Start":
                print("La partita è inziata!")
                print("--------------\n")

            elif recvDataDecode == "Divider":
                print("--------------\n")

            elif recvDataDecode == "X":
                if player == "X":
                    print("È il tuo turno!\n")
                else:
                    print("Turno del giocatore X\n")

            elif recvDataDecode == "O":
                if player == "O":
                    print("È il tuo turno!\n")
                else:
                    print("Turno del giocatore O\n")

            elif "board" in recvDataDecode:
                board = eval(recvDataDecode[5:])
                print_board(board)

            elif "Vince X" in recvDataDecode:
                if player == "X":
                    print("Hai vinto!\n\n")
                else:
                    print("Il giocatore X ha vinto\n\n")
                sys.exit()

            elif "Vince O" in recvDataDecode:
                if player == "O":
                    print("Hai vinto!")
                else:
                    print("Il giocatore O ha vinto\n\n")
                sys.exit()

            elif "Pareggio" in recvDataDecode:
                print("Pareggio")

            elif "Error" in recvDataDecode:
                print(recvDataDecode)

        except socket.error as e:
            print("Socket connection error:", e)
            break

        except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            time.sleep(1)
            break


def start_client():
    try:
        server.connect((host, port))
        print("Connesso a:", host, "porta:", port)
        start_game()
        server.close()
    except socket.error as e:
        print("Socket connection error:", e)


def main():
    start_client()


if __name__ == '__main__':
    main()
