from socket import *
from threading import *

# proxy client
serverName = '127.0.0.1'
serverPort = 1118

# PROXY serveur
proxyPort = 1234
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind(('', proxyPort))
proxySocket.listen(1)
print('Main thread: proxy ready !')


def handle_client(clientConnectionSocket):
   
    message = clientConnectionSocket.recv(2048)
    proxySendSocket = socket(AF_INET, SOCK_STREAM)
    proxySendSocket.connect((serverName, serverPort))
    proxySendSocket.sendall(message)
    # Retour au client
    messageServer = proxySendSocket.recv(2048)
    clientConnectionSocket.sendall(messageServer)
    clientConnectionSocket.close()
           

while True:
    clientConnectionSocket, address = proxySocket.accept()
    Thread(target=handle_client, args=(clientConnectionSocket,)).start()
