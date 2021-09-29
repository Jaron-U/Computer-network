# cited: https://docs.python.org/3.4/howto/sockets.html
#        https://realpython.com/python-sockets/
###############################
## FIle name: Server_chat.py
## Name: Jianglong Yu
## Date: 8/7
## descripution: Set a socket, connenct to client. Send and receive message.
#################################

import socket	#Use the python socket API
import sys
from game import *


def client_first(game, conn):
    print("The chess X selected by the client, so your chess is O.\nWaiting for the client to place the pawn")
    game.display_board()
    game.setClientchess("X")
    game.setServerchess("O")
    while 1:
        n_clientmove = conn.recv(1024)
        n_clientmove = int(n_clientmove.decode())
        print("client drop chess on: ", n_clientmove)
        game.setClientMove(n_clientmove)
        game.board[game.client_move] = game.clientChess
        game.display_board()
        if game.isWinner():
            print("Client win!")
            break
        elif game.isDraw():
            game.display_board()
            print('Draw!')
            break 

        game.getServerMove()
        n_servermove = str(game.server_move)
        conn.sendall(n_servermove.encode())
        game.board[game.server_move] = game.serverChess
        game.display_board()
        if game.isWinner():
            print("Server win!")
            break
        elif game.isDraw():
            print('Draw!')
            break 

def server_first(game, conn):
    print("The chess O selected by the client, so your chess is X.\nYou can place the pawn first")
    game.display_board()
    game.setClientchess("O")
    game.setServerchess("X")
    while 1:
        game.getServerMove()
        n_servermove = str(game.server_move)
        conn.sendall(n_servermove.encode())
        game.board[game.server_move] = game.serverChess
        game.display_board()
        if game.isWinner():
            print("Server win!")
            break
        elif game.isDraw():
            print('Draw!')
            break 

        n_clientmove = conn.recv(1024)
        n_clientmove = int(n_clientmove.decode())
        print("client drop chess on: ", n_clientmove)
        game.setClientMove(n_clientmove)
        game.board[game.client_move] = game.clientChess
        game.display_board()
        if game.isWinner():
            print("Client win!")
            break
        elif game.isDraw():
            game.display_board()
            print('Draw!')
            break 

def main():
    #set HOST and PORT
    HOST = '127.0.0.1'
    PORT = 3081

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind HOST and POST
    try:
        s.bind((HOST, PORT))
    # if failed to bind, print error 
    except socket.error as msg:
        print('Bind failed. Error Code: '+ str(msg[0]) + 'Message: ' + msg[1])
        sys.exit()

    # Start listen to incoming connections
    s.listen(10)
    conn, addr = s.accept()

    # print client infomation 
    print("Server listening on: localhost on port: ", PORT)
    print('Connected by (' + addr[0] + ', ' + str(addr[1]) + ')')

    # Receive the data from server
    print("waiting for message...")

    receive_msg = conn.recv(1024)
    # Print reply data
    print(receive_msg.decode())

    print("Type /q to quit\nEnter message to send...")

    while 1:
        # get user input
        send_msg = input(">")
        if send_msg == '/q':
            # exit chat
            break
        # send message to client
        conn.sendall(send_msg.encode())
        
        # receive message
        receive_msg = conn.recv(1024)
        receive_msg = receive_msg.decode()
        if receive_msg == "client first":
            game = Game()
            client_first(game, conn)
            receive_msg = ""

        elif receive_msg == "server first":
            game = Game()
            server_first(game, conn)
            receive_msg = ""

        # Print reply data
        print(receive_msg)

    conn.close()
    s.close()

main()
