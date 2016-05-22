import socket
import rsa
import threading

def Main():
    host = "127.0.0.1"
    port = 4000

    s = socket.socket()
    s.connect((host, port))

    s.send("PRIVATE")
    

if __name__ == '__main__':
    Main()
