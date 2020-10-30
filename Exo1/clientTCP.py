from socket import *

serverName = '127.0.0.1'
serverPort = 1235



nbMessageToSend =100

for _ in range(nbMessageToSend):
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    message ="ping"
    clientSocket.send(message.encode('utf-8'))
    modifiedMessage = clientSocket.recv(2048)
    print(modifiedMessage.decode('utf-8'))
    clientSocket.close()
