import socket
import threading
import time
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 55000
UDPPORT = 40000


class Client:
    def __init__(self,host,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

        self.sock.connect((host,port))
        msg = tkinter.Tk()
        msg.withdraw()
        self.nickname = simpledialog.askstring("Nickname","Please choose a nickname",parent=msg)
        self.gui_done = False
        self.running = True
        #self.RunFileTransferUDP = threading.Thread(target=self.UDP_FileTransfer_Thread)
        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        Window_bg = "lightgray"
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.win.resizable(False,False)
        self.win.geometry("740x430")
        self.win.title("Messanger")

        self.chat_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.chat_area.config(state='disabled', height=10)

        self.SendTo_label = tkinter.Label(self.win, text="To (blank to all)", bg=Window_bg)
        self.SendTo_label.config(font=("Arial", 12))
        self.msg_label = tkinter.Label(self.win, text="Message", bg=Window_bg)
        self.msg_label.config(font=("Arial", 12))
        self.ServerFile_label = tkinter.Label(self.win, text="Server File", bg=Window_bg)
        self.ServerFile_label.config(font=("Arial", 12))
        self.SaveTo_label = tkinter.Label(self.win, text="Save As", bg=Window_bg)
        self.SaveTo_label.config(font=("Arial", 12))
        self.Welcome_name_label = tkinter.Label(self.win, text="logged as : ["+self.nickname+"]", bg=Window_bg)
        self.Welcome_name_label.config(font=("Arial", 8))

        self.input_area_SendTo = tkinter.Text(self.win, height=1, width=14)
        self.input_area_Message = tkinter.Text(self.win, height=1, width=40)
        self.input_area_ServerFile = tkinter.Text(self.win, height=1, width=14)
        self.input_area_SaveAs = tkinter.Text(self.win, height=1, width=40)

        self.ShowUsers_button = tkinter.Button(self.win, text="Show Users", command=self.ShowUsers)
        self.ShowUsers_button.config(font=('Arial', 12))
        self.ShowServerFiles = tkinter.Button(self.win, text="Show Server Files", command=self.ShowDownloads)
        self.ShowServerFiles.config(font=('Arial', 12))
        self.clear_button = tkinter.Button(self.win, text="Clear", command=self.ClearChat)
        self.clear_button.config(font=('Arial', 12))
        self.send_button = tkinter.Button(self.win,text="Send",command=self.write)
        self.send_button.config(font=('Arial',12))
        self.download_button = tkinter.Button(self.win, text="Download", command=self.DownloadFile)
        self.download_button.config(font=('Arial', 12))

        self.ProgressBar = tkinter.Label(self.win, text="Progress %0", bg=Window_bg)

        self.ShowServerFiles.grid(column=0, row=0,sticky="w",padx=20,pady=10)
        self.ShowUsers_button.grid(column=1, row=0,sticky="w")
        self.Welcome_name_label.grid(column=3, row=0,sticky="w")
        self.clear_button.grid(column=3, row=0,sticky="e",padx=20)

        self.chat_area.grid(column=0,row=1,columnspan=4,padx=20,ipadx=20,pady=5,ipady=20)

        self.SendTo_label.grid(column=0,row=2,sticky="w",padx=20)
        self.msg_label.grid(column=1,row=2,sticky="w")

        self.input_area_SendTo.grid(column=0,row=3,sticky="w",padx=20)
        self.input_area_Message.grid(column=1, row=3,columnspan=2,sticky="w")
        self.send_button.grid(column=3, row=3,sticky="e",padx=20)

        self.ServerFile_label.grid(column=0, row=4,sticky="w",padx=20)
        self.SaveTo_label.grid(column=1, row=4,sticky="w")

        self.input_area_ServerFile.grid(column=0, row=5,sticky="w",padx=20)
        self.input_area_SaveAs.grid(column=1, row=5,columnspan=2,sticky="w")
        self.download_button.grid(column=3, row=5,sticky="e",padx=20)

        self.ProgressBar.grid(column=0, row=6,pady=20,ipady=5,sticky="w",padx=20)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW",self.stop)
        self.win.mainloop()

    def write(self):
        message = "[" + self.nickname + "]"+"<"+self.input_area_SendTo.get('1.0', 'end')[:-1]+\
                  "> :"+self.input_area_Message.get('1.0', 'end') + ""
        self.sock.send(message.encode('utf-8'))
        self.input_area_Message.delete('1.0', 'end')
        #self.input_area_SendTo.delete('1.0', 'end')

    def ShowUsers(self):
        ShowUserstoMeTag = "&ShowUsers&<" + self.nickname + ">"
        self.sock.send(ShowUserstoMeTag.encode('utf-8'))

    def ShowDownloads(self):
        ShowDownloadstoMeTag = "&ShowDownloads&<" + self.nickname + ">"
        self.sock.send(ShowDownloadstoMeTag.encode('utf-8'))

    def UDP_FileReceive(self,SaveAs,ServerFile):

        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        serverAddressPort = (HOST, UDPPORT)
        bufferSize = 1024

        msgFromClient = "Hello UDP Server"
        bytesToSend = str.encode(msgFromClient)
        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        print("Receiving")
        filename = SaveAs
        file = open(filename,'wb')
        file_data = UDPClientSocket.recvfrom(1024)
        print(file_data)

        file.write(file_data[0])

        file.close()

        UDPClientSocket.close()



    def DownloadFile(self):
        message = "&Download&"+"<" + self.nickname + ">" +"(" + self.input_area_SaveAs.get('1.0', 'end')[:-1] + \
                  ") : !" + self.input_area_ServerFile.get('1.0', 'end')[:-1]+"?"
        self.sock.send(message.encode('utf-8'))
        saveAs = self.input_area_SaveAs.get('1.0', 'end')[:-1]
        serverFile = self.input_area_ServerFile.get('1.0', 'end')[:-1]
        self.input_area_ServerFile.delete('1.0', 'end')
        self.input_area_SaveAs.delete('1.0', 'end')
        #self.UDP_FileReceive(saveAs,serverFile)


        DownloadUDP_Temp_Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        DownloadUDP_Temp_Socket.connect((HOST,UDPPORT))
        print("Connected via UDP")
        filename = saveAs
        file = open(filename,'wb')
        file_data = DownloadUDP_Temp_Socket.recv(1024)
        file.write(file_data)
        file.close()
        print("File has been successfully received")
        DownloadUDP_Temp_Socket.close()



    def ClearChat(self):
        self.chat_area.config(state='normal')
        self.chat_area.delete("1.0",'end')
        self.chat_area.config(state='disabled')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        toMeTag = "<"+self.nickname+">"
                        toAllTag = "<>"
                        fromMe = "<"+self.input_area_SendTo.get('1.0', 'end')[:-1]+">"
                        print(message)
                        #print(self.nickname)
                        if message.find(toMeTag)!=-1:
                            print("Sent to me")
                            if message.find("[Server]") != -1:
                                if message.find(toMeTag) != -1:
                                    print("Sent by server")
                                    EditedMessage = message.replace("[Server]","")
                                    EditedMessage = EditedMessage.replace(toMeTag,"")
                                    self.chat_area.config(state='normal')
                                    self.chat_area.insert('end', EditedMessage)
                                    self.chat_area.yview('end')
                                    self.chat_area.config(state='disabled')
                            else:
                                if message.find("[Server]") == -1:
                                    self.chat_area.config(state='normal')
                                    self.chat_area.insert('end', message)
                                    self.chat_area.yview('end')
                                    self.chat_area.config(state='disabled')
                        if message.find(toAllTag)!=-1 and message.find("[Server]") == -1:
                            print("Sent to all")
                            self.chat_area.config(state='normal')
                            self.chat_area.insert('end', message)
                            self.chat_area.yview('end')
                            self.chat_area.config(state='disabled')
                        elif message.find(fromMe)!=-1:
                            if message.find("[Server]") == -1:
                                print("Sent by me")
                                self.chat_area.config(state='normal')
                                self.chat_area.insert('end', message)
                                self.chat_area.yview('end')
                                self.chat_area.config(state='disabled')
            except ConnectionAbortedError:
                print("Connection Aborted")
                break
            except:
                print("Error")
                self.sock.close()
                break



client = Client(HOST,PORT)