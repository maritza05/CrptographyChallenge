# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autoridad_certificadora.ui'
#
# Created: Sat May 21 22:59:10 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

import socket
import threading
import os
from thread import *

import rsa
from Crypto.Cipher import AES
from Crypto import Random
import rsa.randnum


def send_private_key(self):
    host = self.txtDireccionIP.text()
    port = 5000
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
    except socket.error, e:
        print "Unable to Setup Local Socket. Port in Use"
        return

    while 1:
        conn, addr = s.accept()
        if self.lblTipoSolicitud.text() == "PRIVATE":
            conn.send(self.encripted_file)
            recibido = conn.recv(1024)
            if recibido == "OK":
                conn.send(self.encrypted_aes_key)
                recibido = conn.recv(1024)
                if recibido == "OK":
                    conn.send(self.my_public_key.save_pkcs1())

        elif self.lblTipoSolicitud.text() == "PUBLIC":
            to_send_public_key, to_send_aes_key = encrypt_public_key(self)
            conn.send(to_send_public_key)
            recibido = conn.recv(1024)
            if recibido == "OK":
                conn.send(to_send_aes_key)
                recibido = conn.recv(1024)
                if recibido == "OK":
                    conn.send(self.my_public_key.save_pkcs1())

        conn.close()
    s.close()

def server_socket(self):
    host = self.txtDireccionIP.text()
    port = int(self.txtPuerto.text())
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(1)
    except socket.error, e:
        print "Unable to Setup Local Socket. Port in Use"
        return

    while 1:
        conn, addr = s.accept()
        self.label_4.setText("Conectado")
        self.rbtnConectado.setChecked(True)
        self.lblStatus.setText("client connected ip:<" + str(addr) + ">")
        tipo_solicitud = conn.recv(1024)
        self.lblTipoSolicitud.setText(tipo_solicitud)
        conn.send("OK")
        nombre_organizacion = ""
        nombre_organizacion += conn.recv(1024)
        self.lineEdit.setText(nombre_organizacion)
        #conn.send("Gracias")
        #print "Listo!"
    conn.close()
    s.close()



def encrypt_public_key(self):
    organizacion = self.lineEdit.text()

    # Creamos nuestra llave para AES
    aes_key = rsa.randnum.read_random_bits(128)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CFB, iv)

    # Encriptamos con AES la llave publica de la empresa
    text_empresa_public_key = self.public_keys[self.lineEdit.text()]
    self.encripted_public_file = cipher.encrypt(text_empresa_public_key)

    # Encriptamos la llave del algoritmo AES con nuestra llave privada
    self.encrypted_public_aes_key = rsa.encrypt(aes_key, self.my_private_key)
    return self.encripted_public_file, self.encrypted_public_aes_key




try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Generamos nuestras claves publicas y privadas
        self.my_private_key, self.my_public_key = rsa.newkeys(512)

        # Create our dictionary of public keys
        self.public_keys = {}


        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(631, 611)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 611, 61))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtDireccionIP = QtGui.QLineEdit(self.frame)
        self.txtDireccionIP.setGeometry(QtCore.QRect(80, 20, 141, 23))
        self.txtDireccionIP.setObjectName(_fromUtf8("txtDireccionIP"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(240, 20, 54, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.txtPuerto = QtGui.QLineEdit(self.frame)
        self.txtPuerto.setGeometry(QtCore.QRect(290, 20, 113, 23))
        self.txtPuerto.setObjectName(_fromUtf8("txtPuerto"))
        self.btnConectarse = QtGui.QPushButton(self.frame)
        self.btnConectarse.setGeometry(QtCore.QRect(440, 20, 91, 24))
        self.btnConectarse.setObjectName(_fromUtf8("btnConectarse"))

        ################################################################
        # Executes when the GenerarLlaves Button is clicked
        self.btnConectarse.clicked.connect(self.start_server)
        ################################################################


        self.rbtnConectado = QtGui.QRadioButton(self.frame)
        self.rbtnConectado.setGeometry(QtCore.QRect(550, 20, 95, 21))
        self.rbtnConectado.setText(_fromUtf8(""))
        self.rbtnConectado.setObjectName(_fromUtf8("rbtnConectado"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 70, 291, 111))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 54, 15))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_8 = QtGui.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(170, 10, 31, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.lblTipoSolicitud = QtGui.QLabel(self.frame_2)
        self.lblTipoSolicitud.setGeometry(QtCore.QRect(210, 10, 54, 15))
        self.lblTipoSolicitud.setObjectName(_fromUtf8("lblTipoSolicitud"))
        self.label_4 = QtGui.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(70, 10, 91, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.btnGenerarLlaves = QtGui.QPushButton(self.frame_2)
        self.btnGenerarLlaves.setGeometry(QtCore.QRect(80, 80, 111, 24))
        self.btnGenerarLlaves.setObjectName(_fromUtf8("btnGenerarLlaves"))

        ################################################################
        # Executes when the GenerarLlaves Button is clicked
        self.btnGenerarLlaves.clicked.connect(self.generate_new_keys)
        ################################################################

        self.lineEdit = QtGui.QLineEdit(self.frame_2)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 241, 23))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(0, 190, 291, 361))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.btnEnviarLlave = QtGui.QPushButton(self.frame_3)
        self.btnEnviarLlave.setGeometry(QtCore.QRect(70, 320, 141, 24))
        self.btnEnviarLlave.setObjectName(_fromUtf8("btnEnviarLlave"))

        ################################################################
        # Executes when the EnviarLlave Button is clicked
        self.btnEnviarLlave.clicked.connect(self.restart_server_to_send)
        ################################################################

        self.btnEncriptar = QtGui.QPushButton(self.frame_3)
        self.btnEncriptar.setGeometry(QtCore.QRect(90, 143, 91, 31))
        self.btnEncriptar.setObjectName(_fromUtf8("btnEncriptar"))

        ################################################################
        # Executes when the Encriptar Button is clicked
        self.btnEncriptar.clicked.connect(self.encrypt_private_key)
        ################################################################

        self.label_7 = QtGui.QLabel(self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(20, 10, 54, 15))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.txtPlainLlave = QtGui.QTextEdit(self.frame_3)
        self.txtPlainLlave.setGeometry(QtCore.QRect(20, 30, 251, 101))
        self.txtPlainLlave.setObjectName(_fromUtf8("txtPlainLlave"))
        self.txtEncryptedLlave = QtGui.QTextEdit(self.frame_3)
        self.txtEncryptedLlave.setGeometry(QtCore.QRect(20, 180, 241, 131))
        self.txtEncryptedLlave.setObjectName(_fromUtf8("txtEncryptedLlave"))
        self.frame_4 = QtGui.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(310, 70, 311, 481))
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.listLlavesPublicas = QtGui.QListWidget(self.frame_4)
        self.listLlavesPublicas.setGeometry(QtCore.QRect(10, 120, 281, 261))
        self.listLlavesPublicas.setObjectName(_fromUtf8("listLlavesPublicas"))

        ################################################################
        # Executes when the item in listLlavesPublicas is clicked
        self.listLlavesPublicas.itemClicked.connect(self.show_public_key)
        ################################################################

        self.label_5 = QtGui.QLabel(self.frame_4)
        self.label_5.setGeometry(QtCore.QRect(20, 100, 111, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.progressBar = QtGui.QProgressBar(self.frame_4)
        self.progressBar.setGeometry(QtCore.QRect(20, 50, 251, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_6 = QtGui.QLabel(self.frame_4)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 121, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.btnDesconectarse = QtGui.QPushButton(self.frame_4)
        self.btnDesconectarse.setGeometry(QtCore.QRect(90, 400, 121, 41))
        self.btnDesconectarse.setObjectName(_fromUtf8("btnDesconectarse"))
        self.lblStatus = QtGui.QLabel(self.centralwidget)
        self.lblStatus.setGeometry(QtCore.QRect(10, 550, 551, 16))
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 631, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuAcerca = QtGui.QMenu(self.menubar)
        self.menuAcerca.setObjectName(_fromUtf8("menuAcerca"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionVersion = QtGui.QAction(MainWindow)
        self.actionVersion.setObjectName(_fromUtf8("actionVersion"))
        self.actionSalir = QtGui.QAction(MainWindow)
        self.actionSalir.setObjectName(_fromUtf8("actionSalir"))
        self.menuAcerca.addAction(self.actionVersion)
        self.menuAcerca.addAction(self.actionSalir)
        self.menubar.addAction(self.menuAcerca.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoridadCertificadora", None))
        self.label.setText(_translate("MainWindow", "Dirección IP", None))
        self.label_2.setText(_translate("MainWindow", "Puerto:", None))
        self.btnConectarse.setText(_translate("MainWindow", "Conectarse", None))
        self.label_3.setText(_translate("MainWindow", "Status:", None))
        self.label_8.setText(_translate("MainWindow", "Tipo:", None))
        self.lblTipoSolicitud.setText(_translate("MainWindow", "Privada", None))
        self.label_4.setText(_translate("MainWindow", "Esperando", None))
        self.btnGenerarLlaves.setText(_translate("MainWindow", "Generar LLaves", None))
        self.btnEnviarLlave.setText(_translate("MainWindow", "Enviar LLave", None))
        self.btnEncriptar.setText(_translate("MainWindow", ">>", None))
        self.label_7.setText(_translate("MainWindow", "Llave:", None))
        self.label_5.setText(_translate("MainWindow", "Llaves Públicas:", None))
        self.label_6.setText(_translate("MainWindow", "Progreso del envio:", None))
        self.btnDesconectarse.setText(_translate("MainWindow", "Desconectarse", None))
        self.lblStatus.setText(_translate("MainWindow", "status:", None))
        self.menuAcerca.setTitle(_translate("MainWindow", "Acerca..", None))
        self.actionVersion.setText(_translate("MainWindow", "Versión", None))
        self.actionSalir.setText(_translate("MainWindow", "Salir", None))


    # Generar las nuevas llaves para la empresa
    def generate_new_keys(self):
        self.empresa_public_key, self.empresa_private_key = rsa.newkeys(512)
        text_empresa_private_key = self.empresa_private_key.save_pkcs1()
        self.txtPlainLlave.setText(text_empresa_private_key)


    def encrypt_private_key(self):
        organizacion = self.lineEdit.text()

        # Creamos nuestra llave para AES
        aes_key = rsa.randnum.read_random_bits(128)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(aes_key, AES.MODE_CFB, iv)

        # Encriptamos con AES la llave privada de la empresa
        text_empresa_private_key = self.empresa_private_key.save_pkcs1()
        self.encripted_file = cipher.encrypt(text_empresa_private_key)

        # Encriptamos la llave del algoritmo AES con nuestra llave privada
        self.encrypted_aes_key = rsa.encrypt(aes_key, self.my_private_key)

        # Actualizamos la lista con las claves publicas
        self.public_keys[organizacion] = self.empresa_public_key.save_pkcs1()
        self.listLlavesPublicas.addItem(organizacion)

    def show_public_key(self, item):
        item_public_key = self.public_keys[item.text()]
        self.txtEncryptedLlave.setText(item_public_key)

    def start_server(self):
        start_new_thread(server_socket, (self,))
        print  "Server Started Sicessfully"

    def restart_server_to_send(self):
        start_new_thread(send_private_key, (self,))
        print  "Server Started Sicessfully to Send the Private Key"




if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
