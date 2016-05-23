import socket
import rsa
import threading
from Crypto import Random
from Crypto.Cipher import AES

def get_keys(public_key, encripted_aes_key, private_key):
    my_public_key = rsa.PrivateKey.load_pkcs1(public_key)
    print my_public_key
    decrypted_aes_key = rsa.decrypt(encripted_aes_key, my_public_key)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(decrypted_aes_key, AES.MODE_CFB, iv)
    my_private_key = cipher.decrypt(private_key)
    print "===================== LA LLAVE PRIVADA ================================="
    my_private_key = "-----BEGIN RSA PRIVATE KEY-----\n"+my_private_key[my_private_key.find('\n')+1:]
    print my_private_key
    my_private_key = rsa.PrivateKey.load_pkcs1(my_private_key)
    print my_private_key
    return my_private_key




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
        encripted_private_key = s.recv(4096)
        print encripted_private_key
        s.send("OK")
        encripted_aes_key = s.recv(1024)
        print "=============================="
        print encripted_aes_key
        s.send("OK")
        public_key_autoridad = s.recv(1024)
        print public_key_autoridad
        print "==============================="
        my_private_key = get_keys(public_key_autoridad, encripted_aes_key, encripted_private_key)
        s.close()

        esperar_mensaje = raw_input("Desea esperar un mensaje? > ")
        if esperar_mensaje == "OK":
            host = "127.0.0.1"
            port = int(raw_input("En que puerto desea esperar ? > "))
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind((host, port))
                s.listen(1)
            except socket.error, e:
                print "Unable to Setup Local Socket. Port in Use"
                return

            while 1:
                conn, addr = s.accept()
                mensaje = conn.recv(4096)
                mensaje_desencriptado = rsa.decrypt(mensaje, my_private_key)
                print "============== MENSAJE ENCRIPTADO ===================="
                print mensaje
                print "============== MENSAJE DESENCRIPTADO ================="
                print mensaje_desencriptado
            s.close()

    else:
        s.close()




def Main():
    send_org_name()


if __name__ == '__main__':
    Main()
