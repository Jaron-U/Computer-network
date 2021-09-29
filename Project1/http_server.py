# cited from https://www.binarytides.com/python-socket-programming-tutorial/
# name: Jianglong Yu
# file name: http_server.py

import socket	#Use the python socket API
import sys

#set HOST and PORT
HOST = ""
PORT = 8001

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
print('Connected by (' + addr[0] + ',' + str(addr[1]) + ')')

data = "HTTP/1.1 200 OK\r\n"\
 "Content-Type: text/html; charset=UTF-8\r\n\r\n"\
 "<html>Congratulations! You've downloaded the first Wireshark lab file!</html>\r\n"

#Send data to client
conn.sendall(data.encode())

# Receive the data from server
reply = conn.recv(1024)

# Print reply data
print("\nReceived:", reply)
print("\nSending>>>>>>>>\n", data, "\n<<<<<<<<")

conn.close()
s.close()