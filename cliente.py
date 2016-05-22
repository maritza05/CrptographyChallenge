import socket
import rsa
import threading

def send_org_name():
    host = "127.0.0.1"
    port = 4000

    s = socket.socket()
    s.connect((host, port))

    s.send("PRIVATE")
    status = s.recv(1024)
    s.send("organizacion1")
    s.close()

def recv_key():
    host = "127.0.0.1"
    port = 5000

    s = socket.socket()
    s.connect((host, port))
    message = s.recv(1024)
    print message
    s.close()

def Main():
    send_org_name()
    recv_key()

if __name__ == '__main__':
    Main()
