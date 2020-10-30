from socket import *
from threading import *
from datetime import datetime

# proxy client
serverName='127.0.0.1'
serverPort= 5679

## PROXY serveur
proxyPort = 1239
proxySocket = socket(AF_INET,SOCK_STREAM)
proxySocket.bind(('',proxyPort))
proxySocket.listen(1)
print('proxy ready')



def handle_client(clientConnectionSocket):
        data = open("data.txt",'w+')
        message = clientConnectionSocket.recv(4096)
        heure = 'Client: '+ str(datetime.now())
        decode = message.decode('utf-8')
        data.write(heure)
        data.write(decode)
        proxySendSocket = socket(AF_INET,SOCK_STREAM)
        proxySendSocket.connect((serverName,serverPort))
        proxySendSocket.send(message)
        messageServer = proxySendSocket.recv(4096)
        data.write('Server : 4096' + messageServer.decode('utf-8'))
        data.close()
        clientConnectionSocket.sendall(messageServer)
        clientConnectionSocket.close()
        

while True:
        clientConnectionSocket, address = proxySocket.accept()
        Thread(target=handle_client,args=(clientConnectionSocket,)).start()


