from socket import *
from threading import *

# proxy client
serverName='127.0.0.1'
serverPort= 8888

## PROXY serveur
proxyPort = 5679
proxySocket = socket(AF_INET,SOCK_STREAM)
proxySocket.bind(('',proxyPort))
proxySocket.listen(1)
print("censure start")
interdictionfile = ['vieprive.txt','interdit.txt','confidentiel.txt']
def decode(message):
    messageUTF8 = message.decode('utf-8')
    messageSplitedByLine = messageUTF8.split("\n")
    messageFirstLine = messageSplitedByLine[0].split(" ")
    return messageFirstLine[1][1:]
def handle_client(clientConnectionSocket):
    
    message = clientConnectionSocket.recv(4096)
    requestedFileName =decode(message)
    for i in interdictionfile:
        if (requestedFileName == i ) :
            errorMessage = "HTTP/1.1 404 NOT FOUND\r\nServer : Microsoft-IIS/5.0\r\nDate : Sat, 12 oct 2019 14:37:12 GMT\r\nContent-Type : text/html; charset=iso-8859-1\r\nContent-Length : 4094\r\nLast-Modified : Fri, 14 Jan 2007 08:25:13 GMT\r\n\r\n"
            errorMessage = errorMessage + "Erreur 404 - Fichier interdit (voir l'état de la requête dans le navigateur)"
            clientConnectionSocket.sendall(errorMessage.encode('utf-8'))
            clientConnectionSocket.close()
            return
    proxySendSocket = socket(AF_INET,SOCK_STREAM)
    proxySendSocket.connect((serverName,serverPort))
    proxySendSocket.send(message)
    messageServer = proxySendSocket.recv(4096)
    clientConnectionSocket.sendall(messageServer)
    clientConnectionSocket.close()

while True:
        clientConnectionSocket, address = proxySocket.accept()
        Thread(target=handle_client,args=(clientConnectionSocket,)).start()