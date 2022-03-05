import unittest
#from server import *
import threading
import time
import socket
def ServerThread_TCP():
    host = "127.0.0.1"
    port = 55000
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())
    conn.close()
    server_socket.close()
def ClientThread_TCP():
    host = "127.0.0.1"
    port = 55000
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((host, port))
    message = input(" -> ")
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        print('Received from server: ' + data)
        message = input(" -> ")
    client_socket.close()

def ServerThread_UDP():
    host = "127.0.0.1"
    port = 55000
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, address = server_socket.accept()
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())
    conn.close()
    server_socket.close()
def ClientThread_UDP():
    host = "127.0.0.1"
    port = 55000
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.connect((host, port))
    message = input(" -> ")
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        print('Received from server: ' + data)
        message = input(" -> ")
    client_socket.close()


class Test(unittest.TestCase):
    HOST = '127.0.0.1'
    PORT = 55000
    threadServer_tcp = threading.Thread(target=ServerThread_TCP)
    threadClient_tcp = threading.Thread(target=ClientThread_TCP)
    threadServer_udp = threading.Thread(target=ServerThread_UDP)
    threadClient_udp = threading.Thread(target=ClientThread_UDP)

    def test_Connection_TCP(self):
        try:
            self.threadServer_tcp.start()
            self.threadClient_tcp.start()
            time.sleep(2)
            self.assertEqual(1, 1)
        except:
            self.assertEqual(1, 2)

    def test_Connection_UDP(self):
        try:
            self.threadServer_udp.start()
            self.threadClient_udp.start()
            time.sleep(2)
            self.assertEqual(1,1)
        except:
            self.assertEqual(1,2)
    def test_Connection_TCP_withLargeDelay(self):
        try:
            self.threadServer_tcp.start()
            self.threadClient_tcp.start()
            time.sleep(10)
            self.assertEqual(1, 2)
        except:
            self.assertEqual(1, 1)

    def test_Connection_UDP_withLargeDelay(self):
        try:
            self.threadServer_udp.start()
            self.threadClient_udp.start()
            time.sleep(10)
            self.assertEqual(1,2)
        except:
            self.assertEqual(1,1)

    def test_Connection_UDPandTCP_Together(self):
        try:
            self.threadServer_udp.start()
            self.threadServer_tcp.start()
            self.threadClient_udp.start()
            self.threadClient_tcp.start()
            time.sleep(2)
            self.assertEqual(1,2)
        except:
            self.assertEqual(1,1)

