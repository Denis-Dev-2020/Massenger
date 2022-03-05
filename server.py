import socket
import sys
import threading
import time

HOST = '127.0.0.1'
PORT = 55000
UDPPORT = 40000
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
if sys.platform.startswith('linux') :
    print("Hello linux")
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.bind((HOST,PORT))
server.listen()
clients = []
nicknames = []
files4Download = []
files4Download.append(r"sendme1.txt")
files4Download.append(r"sendme2.txt")
files4Download.append(r"sendme3.txt")





def UDP_FileTransfer_Thread(requestString,File,SaveTo):
    print(requestString)
    NameOfRequesterUserIndex = requestString.index('<')
    NameOfRequesterUserIndex2 = requestString.index('>')
    NameOfRequesterUser = "<" + requestString[NameOfRequesterUserIndex + 1:NameOfRequesterUserIndex2] + ">"
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1024)
    UDPServerSocket.bind((HOST, UDPPORT))
    print("Want to download "+File)
    print("Want to save as"+SaveTo)
    try:
        filename = File
        file = open(filename, 'rb')
        file_data = file.read(40000)
        packetsList = []
        packetCheckSumList = []
        LastByte = len(file_data)%1024
        NumberOfPackets = 0
        CheckSum = 0
        if LastByte == 0:
            NumberOfPackets = round(len(file_data) / 1024)
            for i in range(0, NumberOfPackets):
                a = file_data[i * 1024:(i * 1024) + 1024]
                packetsList.append(a)
                for i in range(0, len(a)):
                    CheckSum = CheckSum + a[i]
                packetCheckSumList.append(CheckSum)
                CheckSum = 0
        else:
            NumberOfPackets = round(len(file_data) / 1024)+1
            for i in range(0, NumberOfPackets):
                a = file_data[i * 1024:(i * 1024) + 1024]
                packetsList.append(a[:LastByte])
                for i in range(0, len(a)):
                    CheckSum = CheckSum + a[i]
                packetCheckSumList.append(CheckSum)
                CheckSum = 0
            packetsList.append(file_data)
        print("Number of packets : ["+str(NumberOfPackets)+"]")
        print("Last Byte         : ["+str(LastByte)+"]")
        print(packetsList)
        print(packetCheckSumList)
        broadcast(("[Server]" +str(NameOfRequesterUser) +"________________________________\n"
                   "| Last Byte :              |"+str(LastByte)+"\n").encode('utf-8'))

        UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPServerSocket.bind((HOST, UDPPORT))

        while True:
            msgggg = UDPServerSocket.recvfrom(1024)
            clientAddr = msgggg[1]
            datttta = msgggg[0]
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(clientAddr)
            print(datttta)
            UDPServerSocket.sendto(file_data, clientAddr)


        # msgFromServer = "Hello UDP Client"
        # bytesToSend = str.encode(msgFromServer)
        # print("UDP server up and listening")
        # msgFromServer = "Hello UDP Client"
        # bytesToSend = str.encode(msgFromServer)
        # UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # UDPServerSocket.bind((HOST, UDPPORT))
        # print("UDP server up and listening")
        # while (True):
        #     bytesAddressPair = UDPServerSocket.recvfrom(1024)
        #     message = bytesAddressPair[0]
        #     address = bytesAddressPair[1]
        #     clientMsg = "Message from Client:{}".format(message)
        #     clientIP = "Client IP Address:{}".format(address)
        #     print(clientMsg)
        #     print(clientIP)
        #     UDPServerSocket.sendto(bytesToSend, address)




    except:
        print("Error Communicating")

    UDPServerSocket.close()









def broadcast(massage):
    for client in clients:
        client.send(massage)
def ShowUsers(requestString):
    print(requestString)
    NameOfRequesterUserIndex = requestString.index('<')
    NameOfRequesterUserIndex2 = requestString.index('>')
    NameOfRequesterUser = "<"+requestString[NameOfRequesterUserIndex+1:NameOfRequesterUserIndex2]+">"
    broadcast(("[Server]"+NameOfRequesterUser+" ________________________________\n"
              "| Connected users :              |\n").encode('utf-8'))
    for i in range(0, len(nicknames)):
        User = bytes(nicknames[i]).decode()
        broadcast(("[Server]"+NameOfRequesterUser+f"\t{User}\n").encode('utf-8'))
    broadcast(("[Server]"+NameOfRequesterUser+"|________________________________|\n").encode('utf-8'))
def ShowDownloads(requestString):
    print(requestString)
    NameOfRequesterUserIndex = requestString.index('<')
    NameOfRequesterUserIndex2 = requestString.index('>')
    NameOfRequesterUser = "<" + requestString[NameOfRequesterUserIndex + 1:NameOfRequesterUserIndex2] + ">"
    broadcast(("[Server]" + NameOfRequesterUser +
                " _______________________________________________________________________________\n"
                "|                              Downloadable Files :                             |\n").encode('utf-8'))

    for i in range(0, len(files4Download)):
        broadcast(("[Server]" + NameOfRequesterUser + f"\t{files4Download[i]}\n").encode('utf-8'))

    broadcast(("[Server]" + NameOfRequesterUser +
               "|_______________________________________________________________________________|\n").encode('utf-8'))
def DownloadingFile(requestString):
    print(requestString)
    NameOfRequesterUserIndex = requestString.index('<')
    NameOfRequesterUserIndex2 = requestString.index('>')
    NameOfRequesterUser = "<" + requestString[NameOfRequesterUserIndex + 1:NameOfRequesterUserIndex2] +">"
    NameOfRequesterFileIndex = requestString.index('!')
    NameOfRequesterFileIndex2 = requestString.index('?')
    NameOfRequesterFile = ""+requestString[NameOfRequesterFileIndex + 1:NameOfRequesterFileIndex2]
    NameOfRequesterSavePathIndex = requestString.index('(')
    NameOfRequesterSavePathIndex2 = requestString.index(')')
    NameOfRequesterSavePath = ""+requestString[NameOfRequesterSavePathIndex + 1:NameOfRequesterSavePathIndex2]
    RunFileTransferUDP = threading.Thread(target=UDP_FileTransfer_Thread,
                                          args=(NameOfRequesterUser,NameOfRequesterFile,NameOfRequesterSavePath,))
    print("File:")
    print(NameOfRequesterFile)
    print("Save As:")
    print(NameOfRequesterSavePath)
    broadcast(("[Server]" + NameOfRequesterUser +
                " _______________________________________________________________________________\n"
                "|                              Downloading File   :                             |\n").encode('utf-8'))
    broadcast(("[Server]" + NameOfRequesterUser +"\t"+NameOfRequesterFile+"\n").encode('utf-8'))
    broadcast(("[Server]" + NameOfRequesterUser +
               "|                               Saving File As  :                               |\n").encode('utf-8'))
    broadcast(("[Server]" + NameOfRequesterUser +"\t"+ NameOfRequesterSavePath+"\n").encode('utf-8'))

    broadcast(("[Server]" + NameOfRequesterUser +
               "|_______________________________________________________________________________|\n").encode('utf-8'))
    print(clients[0])
    RunFileTransferUDP.start()
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message.decode('utf-8').find("&ShowUsers&") != -1:
                ShowUsers(message.decode('utf-8'))
            elif message.decode('utf-8').find("&ShowDownloads&")!=-1:
                ShowDownloads(message.decode('utf-8'))
            elif message.decode('utf-8').find("&Download&")!=-1:
                DownloadingFile(message.decode('utf-8'))
            else:
                print(f"{nicknames[clients.index(client)]} says {message}")
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"<>[{nickname.decode('utf-8')}] disconnected the server!\n".encode('utf-8'))
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)
        print(f"Nick name of the client is {nickname}")
        broadcast(f"<>[{nickname.decode('utf-8')}] connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server\n".encode('utf-8'))
        thread = threading.Thread(target=handle,args=(client,))
        thread.start()
        if len(nicknames)>0:
            if len(nicknames) == 0:
                server.shutdown(socket.SHUT_RDWR)
                server.close()
                break
print("Server running ..")
receive()