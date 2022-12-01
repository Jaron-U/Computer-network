CS37 2 - Project

How to run?
Step 1 : python3 Server_chat.py
Step 2: python3 Client_chat.py
Screenshot of my running code:
Server:
Client:
Extra Credit:
Step 1 : python3 Server_chat.py
Step 2: python3 Client_chat.py

Before starting the game, client and server should send a message to each other.
Type “/game” in the Client, which can start the game Tic-tac-toe. Client will send an
invitation message to server. After server agree to join in the game, the Client can choose
the chess. Chess “X” moves first. If server refuse the Client’s invitation. The client side can
send message to server.
After the game is over, the server side can send messages to client. (Note: In the game, both
of server and client cannot exit the game by typing “/q”).
I assume the players can input the valid characters or numbers following the prompt.
Screenshot:
Client chess: “X”

Client chess: “O”

Error:
If the is an error: “Bind failed. Error Code: XXXX”, please try to change the port number
in the line 82 in Server_chat.py and line 117 in Client_chat.py, confirm they are the same
number.


