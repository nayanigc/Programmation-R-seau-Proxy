from socket import *
from threading import *

# proxy client
serverName='127.0.0.1'
serverPort= 9999

## PROXY serveur
proxyPort = 8888
proxySocket = socket(AF_INET,SOCK_STREAM)
proxySocket.bind(('',proxyPort))
proxySocket.listen(1)
success = '200'
file = list()
acceptation = "HTTP/1.1 200 OK\r\nServer : Microsoft-IIS/5.0\r\nDate : Sat, 15 Jan 2007 14:37:12 GMT\r\nContent-Type : text/html; charset=iso-8859-1\r\nContent-Length : 4094\r\nLast-Modified : Fri, 14 Jan 2007 08:25:13 GMT\r\n\r\n"
print("cache start")

def decode(message):
        messageUTF8 = message.decode('utf-8')
        messageSplitedByLine = messageUTF8.split("\n")
        messageFirstLine = messageSplitedByLine[0].split(" ")
        requestedFileName = messageFirstLine[1][1:]
        print(requestedFileName)
        return requestedFileName

def decodeServer(messageServer):
        messageUTF8 = messageServer.decode('utf-8')
        messageSplitedByLine = messageUTF8.split("\n")
        messageFirstLine = messageSplitedByLine[0].split(" ")
        requestedFileName = messageFirstLine[1]
        print(requestedFileName)
        return requestedFileName
        

def contenu(messageServer):
        messageUTF8 = messageServer.decode('utf-8')
        messageSplitedByLine = messageUTF8.split("\r\n\r\n")
        taille = len (messageSplitedByLine)
        messageFirstLine =  messageSplitedByLine [1]
        return messageFirstLine 
        

def handle_client (clientConnectionSocket):

        message = clientConnectionSocket.recv(4096)
        print(message)
        requestedFileName = decode(message)
        print(requestedFileName)
        print(file)
        if requestedFileName in file:
        ## ecrire sur le fichier client a la suite le GET name  + l heure de la requete 
                requestedFile = open(requestedFileName)
                requestedFileContent = requestedFile.read()
                httpResponse = acceptation + requestedFileContent    
                clientConnectionSocket.sendall(httpResponse.encode('utf-8'))
                
        else:
                proxySendSocket = socket(AF_INET,SOCK_STREAM)
                proxySendSocket.connect((serverName,serverPort))
                proxySendSocket.send(message)
                messageServer = proxySendSocket.recv(2048)
                requestedSuccess = decodeServer(messageServer)
                requestContent = contenu(messageServer)
                if requestedSuccess == success:
                        file.append(requestedFileName)
                        createdFiles = open(requestedFileName,"w+")
                        createdFiles.write(requestContent)
                clientConnectionSocket.sendall(messageServer)
                clientConnectionSocket.close()

      
        
while True:
        clientConnectionSocket, address = proxySocket.accept()
        Thread(target=handle_client,args=(clientConnectionSocket,)).start()

