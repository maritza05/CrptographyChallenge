# -*- coding: utf-8 -*-

import socket
import rsa
import threading
from Crypto import Random
from Crypto.Cipher import AES
import click

def get_keys(public_key, encripted_aes_key, private_key):
    my_public_key = rsa.PrivateKey.load_pkcs1(public_key)
    decrypted_aes_key = rsa.decrypt(encripted_aes_key, my_public_key)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(decrypted_aes_key, AES.MODE_CFB, iv)
    print "\n\nDesencriptando llave publica..."
    with click.progressbar(range(100000)) as bar:
        for i in bar:
            pass
    my_private_key = cipher.decrypt(private_key)
    print "\n\n===================== LA LLAVE PUBLICA ================================="
    my_private_key = "-----BEGIN RSA PUBLIC KEY-----\n"+my_private_key[my_private_key.find('\n')+1:]
    print my_private_key
    my_private_key = rsa.PublicKey.load_pkcs1(my_private_key)
    return my_private_key




def send_org_name():
    print """
        ██████╗██╗     ██╗███████╗███╗   ██╗████████╗███████╗
        ██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
        ██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║   █████╗
        ██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║   ██╔══╝
        ╚██████╗███████╗██║███████╗██║ ╚████║   ██║   ███████╗
         ╚═════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

    """
    host = raw_input("El host de la autoridad certificadora? >>> ")
    port = int(raw_input("Puerto de la autoridad certificadora? >>> "))

    s = socket.socket()
    s.connect((host, port))

    print "Desea solicitar una llave privada o publica?"
    print " (A) Llave Privada"
    print " (B) Llave Publica"
    solicitud_llave = raw_input(">>> ")
    if solicitud_llave == "A":
        s.send("PRIVATE")
    else:
        s.send("PUBLIC")

    status = s.recv(1024)
    nombre_organizacion = raw_input("Cual es el nombre de la organizacion de la que desea la llave? >>> ")
    s.send(nombre_organizacion)

    solicitud = raw_input("La Autoridad Certificadora ha recuperado la llave... \nDesea solicitarla (OK/N)? >>> ")
    if solicitud == "OK":
        port = 5000
        s = socket.socket()
        s.connect((host, port))
        encripted_private_key = s.recv(4096)
        print "\n\n========================= INFO ===============================================\n\n"
        print "========== ESTA ES LA LLAVE PUBLICA DE LA EMPRESA ENCRIPTADA CON AES ========="
        print encripted_private_key
        s.send("OK")
        encripted_aes_key = s.recv(1024)
        print "\n\n=========== ESTA ES LA LLAVE AES ENCRIPTADA CON RSA =========================="
        print encripted_aes_key
        s.send("OK")
        public_key_autoridad = s.recv(1024)
        public_key_organizacion = get_keys(public_key_autoridad, encripted_aes_key, encripted_private_key)
        #s.close()

        host = raw_input("El host del cliente? > ")
        port = int(raw_input("Puerto del cliente? > "))

        s2 = socket.socket()
        s2.connect((host, port))
        mensaje = raw_input("Que mensaje desea enviar? > ")
        encrypted_mensaje = rsa.encrypt(mensaje, public_key_organizacion)
        s2.send(encrypted_mensaje)
        s2.close()

    s.close()




def Main():
    send_org_name()


if __name__ == '__main__':
    Main()
