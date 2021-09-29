# cited from https://www.binarytides.com/python-socket-programming-tutorial/
# name: Jianglong Yu
# file name: http_client2.py

import socket	#use the python socket API
import sys

try:
	#create an AF_INET, STREAM socket (TCP)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # the error situation
except socket.error as msg:
	print('Failed to create socket. Error code: '+ str(msg[0]) + ' , Error message : ' + msg[1])
	sys.exit()

# set the host and port number
host = 'gaia.cs.umass.edu'
port = 80

# get the ip from host
try:
	remote_ip = socket.gethostbyname(host)
except socket.gaierror:
	# if can not be resolved
	print('Hostname could not be resolved. Exiting')
	sys.exit()
	
#Connect to remote server
s.connect((remote_ip , port))

#Send request to remote server
request = "GET /wireshark-labs/HTTP-wireshark-file3.html HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"

try :
	#Set the whole string
	s.sendall(request.encode())
except socket.error:
	#Send failed
	print('Send failed')
	sys.exit()

# print the request and host info
print("Request:" + request)

# get the receiving data 
all_reply = ''
# keep receiving data until the length of reply is equal 0
while 1:
    reply = s.recv(4096)
    if len(reply) <= 0:
        break
    all_reply += reply.decode()

# print the length of receving data
print ("[RECV] - length:", len(all_reply))
print(all_reply)

s.close()
