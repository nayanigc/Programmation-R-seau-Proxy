from socket import *
from threading import *


serverPort = 9999
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

print('server ready')
http = 'HTTP'
httpoOkHeader = "HTTP/1.1 200 OK\r\nServer : Microsoft-IIS/5.0\r\nDate : Sat, 15 Jan 2007 14:37:12 GMT\r\nContent-Type : text/html; charset=iso-8859-1\r\nContent-Length : 4094\r\nLast-Modified : Fri, 14 Jan 2007 08:25:13 GMT\r\n\r\n"
def handle_server (connectionSocket):
        message = connectionSocket.recv(4096)
        messageUTF8 = message.decode('utf-8')
        messageSplitedByLine = messageUTF8.split("\n")
        messageFirstLine = messageSplitedByLine[0].split(" ")
        requestedFileName = messageFirstLine[1][1:]

        try:
                requestedFile = open(requestedFileName)
                requestedFileContent = requestedFile.read()
                httpResponse = httpoOkHeader + requestedFileContent
                connectionSocket.sendall(httpResponse.encode('utf-8'))
        except:
                errorMessage = "HTTP/1.1 404 NOT FOUND\r\nServer : Microsoft-IIS/5.0\r\nDate : Sat, 12 oct 2019 14:37:12 GMT\r\nContent-Type : text/html; charset=iso-8859-1\r\nContent-Length : 4094\r\nLast-Modified : Fri, 14 Jan 2007 08:25:13 GMT\r\n\r\n"
                errorMessage = errorMessage + "Erreur 404 - Fichier non trouvé (voir l'état de la requête dans le navigateur)"
                connectionSocket.sendall(errorMessage.encode('utf-8'))
                
while True:
        connectionSocket, address = serverSocket.accept()
        Thread(target=handle_server,args=(connectionSocket,)).start()

