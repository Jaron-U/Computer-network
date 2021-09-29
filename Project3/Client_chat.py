# cited: https://docs.python.org/3.4/howto/sockets.html
#        https://realpython.com/python-sockets/
###############################
## FIle name: Client_chat.py
## Name: Jianglong Yu
## Date: 8/7
## descripution: Set a socket, connenct to server. Send and receive message.
#################################

import socket	#use the python socket API
import sys
from game import *

def game_play(s, game):
    game.getClientchess()
    if game.clientChess in ("X", "x"):
        game.setClientchess("X")
        game.setServerchess("O")
        send_chess_info = "client first"
        s.sendall(send_chess_info.encode())
        game.display_board()
        while 1:
            game.getClientMove()
            n_clientmove = str(game.client_move)
            s.sendall(n_clientmove.encode())
            game.board[game.client_move] = game.clientChess
            game.display_board()
            if game.isWinner():
                print("Client win!")
                break
            elif game.isDraw():
                game.display_board()
                print('Draw!')
                break 

            n_servermove = s.recv(1024)
            n_servermove = int(n_servermove.decode())
            print("server drop chess on: ", n_servermove)
            game.setServerMove(n_servermove)
            game.board[game.server_move] = game.serverChess
            game.display_board()
            if game.isWinner():
                print("Server win!")
                break
            elif game.isDraw():
                game.display_board()
                print('Draw!')
                break 

    # if client choose O            
    else:
        game.setClientchess("O")
        game.setServerchess("X")
        send_chess_info = "server first"
        s.sendall(send_chess_info.encode())
        game.display_board()
        while 1:
            n_servermove = s.recv(1024)
            n_servermove = int(n_servermove.decode())
            print("server drop chess on: ", n_servermove)
            game.setServerMove(n_servermove)
            game.board[game.server_move] = game.serverChess
            game.display_board()
            if game.isWinner():
                print("Server win!")
                break
            elif game.isDraw():
                print('Draw!')
                break 

            game.getClientMove()
            n_clientmove = str(game.client_move)
            s.sendall(n_clientmove.encode())
            game.board[game.client_move] = game.clientChess
            game.display_board()
            if game.isWinner():
                print("Client win!")
                break
            elif game.isDraw():
                print('Draw!')
                break 

def game_invitation(s, game, flag):
     # send a game invitation
    send_msg = "Client invited you join the Tic-tac-toe game.(Accept press 1, Refuse press 0)"
    s.sendall(send_msg.encode())
    # receive the reply
    received_msg = s.recv(1024)
    received_msg = int(received_msg.decode())
    if received_msg == 1:
        # if server accepted the invitation
        received_msg = "Server accepted your game invitation!"
        print(received_msg)

        print("start game!")
        # start game!
        game_play(s, game)
    else:
        # if the server refused the invitation
        received_msg = "Server refused your game invitation!"
        print(received_msg)
        flag[0] = "True"

def main():
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # the error situation
    except socket.error as msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()

    # set the host and port number
    host = '127.0.0.1'
    port = 3081

    #Connect to remote server
    s.connect((host , port))
    # print connect info
    print("Connected to: localhost on port: ", port)

    print("Type /q to quit\nType /game to start Tic-tac-toe\nEnter message to send...")

    while 1:
        refused_flag = ["False"]
        # get user input
        send_msg = input(">")
    
        if (send_msg == "/q"):
            # exit chat
            break

        # if want start a game
        if (send_msg == "/game"):
            game = Game()
            game_invitation(s, game, refused_flag)
            send_msg = ""
            if refused_flag[0] == "True":
                send_msg = input(">")
            if (send_msg == "/q"):
                # exit chat
                break
            
        s.sendall(send_msg.encode())

        # get the receiving data from server
        received_msg = s.recv(1024)
        print(received_msg.decode())

    s.close()

main()
