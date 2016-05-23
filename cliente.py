import socket
import rsa
import threading

def send_org_name():
    host = raw_input("El host de la autoridad certificadora? > ")
    port = int(raw_input("Puerto de la autoridad certificadora? > "))

    s = socket.socket()
    s.connect((host, port))

    print "Desea solicitar una llave privada o publica ? >"
    print " (A) Llave Privada"
    print " (B) Llave Publica"
    solicitud_llave = raw_input("> ")
    if solicitud_llave == "A":
        s.send("PRIVATE")
    else:
        s.send("PUBLIC")

    status = s.recv(1024)
    nombre_organizacion = raw_input("Cual es el nombre de la organizacion? >")
    s.send(nombre_organizacion)

    solicitud = raw_input("Desea solicitar la llave?")
    if solicitud == "OK":
        port = 5000
        s = socket.socket()
        s.connect((host, port))
        message = s.recv(4096)
        print message
        s.close()
    else:
        s.close()




def Main():
    send_org_name()


if __name__ == '__main__':
    Main()
