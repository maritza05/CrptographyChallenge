# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'empresa.ui'
#
# Created: Sun May 22 13:52:41 2016
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


def send_org_info(self):
    host = self.txtDireccionIP.text()
    port = int(self.txtPuerto.text())

    s = socket.socket()
    s.connect((host, port))

    if self.rbtnLlavePrivada.isChecked() == True:
        s.send("PRIVATE")
    elif self.rbtnLlavePublica.isChecked() == True:
        s.send("PUBLIC")

    nombre_organizacion = self.txtNombreOrganizacion.text()
    status = s.recv(1024)
    s.send(nombre_organizacion)

    s.close()
    return

def request_key(self):
    host = self.txtDireccionIP.text()
    port = 5000

    s = socket.socket()
    s.connect((host, port))
    message = s.recv(4096)
    self.my_private_key = message
    print message

    s.close()
    return


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
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(690, 619)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(50, 10, 611, 61))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.txtDireccionIP = QtGui.QLineEdit(self.frame)
        self.txtDireccionIP.setGeometry(QtCore.QRect(80, 20, 221, 23))
        self.txtDireccionIP.setObjectName(_fromUtf8("txtDireccionIP"))
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(340, 20, 54, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.txtPuerto = QtGui.QLineEdit(self.frame)
        self.txtPuerto.setGeometry(QtCore.QRect(410, 20, 113, 23))
        self.txtPuerto.setObjectName(_fromUtf8("txtPuerto"))
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(50, 80, 311, 151))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.txtNombreOrganizacion = QtGui.QLineEdit(self.frame_2)
        self.txtNombreOrganizacion.setGeometry(QtCore.QRect(120, 20, 171, 23))
        self.txtNombreOrganizacion.setObjectName(_fromUtf8("txtNombreOrganizacion"))
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 111, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.btnEnviarDatosOrganizacion = QtGui.QPushButton(self.frame_2)
        self.btnEnviarDatosOrganizacion.setGeometry(QtCore.QRect(100, 110, 91, 24))
        self.btnEnviarDatosOrganizacion.setObjectName(_fromUtf8("btnEnviarDatosOrganizacion"))
        ################################################################
        # Executes when the Encriptar Button is clicked
        self.btnEnviarDatosOrganizacion.clicked.connect(self.start_request_to_info)
        ################################################################


        self.rbtnLlavePrivada = QtGui.QRadioButton(self.frame_2)
        self.rbtnLlavePrivada.setGeometry(QtCore.QRect(40, 70, 101, 21))
        self.rbtnLlavePrivada.setObjectName(_fromUtf8("rbtnLlavePrivada"))

        ################################################################
        # Executes when the radio button rbtnLlavePrivada is clicked

        ################################################################

        self.rbtnLlavePublica = QtGui.QRadioButton(self.frame_2)
        self.rbtnLlavePublica.setGeometry(QtCore.QRect(160, 70, 95, 21))
        self.rbtnLlavePublica.setObjectName(_fromUtf8("rbtnLlavePublica"))

        ################################################################
        # Executes when the radio button rbtnLlavePublica is clicked

        ################################################################


        self.frame_3 = QtGui.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(50, 240, 311, 311))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.btnSolicitarLlave = QtGui.QPushButton(self.frame_3)
        self.btnSolicitarLlave.setGeometry(QtCore.QRect(100, 10, 91, 24))
        self.btnSolicitarLlave.setObjectName(_fromUtf8("btnSolicitarLlave"))

        ################################################################
        # Executes when the button btnSolicitarLlave is clicked
        self.btnSolicitarLlave.clicked.connect(self.start_keys_request)
        ################################################################



        self.txtLlaveEncriptada = QtGui.QTextEdit(self.frame_3)
        self.txtLlaveEncriptada.setGeometry(QtCore.QRect(10, 60, 281, 61))
        self.txtLlaveEncriptada.setObjectName(_fromUtf8("txtLlaveEncriptada"))
        self.label_4 = QtGui.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(20, 40, 111, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 54, 15))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.txtLlaveAES = QtGui.QTextEdit(self.frame_3)
        self.txtLlaveAES.setGeometry(QtCore.QRect(10, 150, 281, 51))
        self.txtLlaveAES.setObjectName(_fromUtf8("txtLlaveAES"))
        self.btnDesencriptarLlave = QtGui.QPushButton(self.frame_3)
        self.btnDesencriptarLlave.setGeometry(QtCore.QRect(90, 210, 111, 24))
        self.btnDesencriptarLlave.setObjectName(_fromUtf8("btnDesencriptarLlave"))

        ################################################################
        # Executes when the button btnSolicitarLlave is clicked
        self.btnDesencriptarLlave.clicked.connect(self.set_key)
        ################################################################


        self.progressBar = QtGui.QProgressBar(self.frame_3)
        self.progressBar.setGeometry(QtCore.QRect(20, 260, 271, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.frame_4 = QtGui.QFrame(self.centralwidget)
        self.frame_4.setGeometry(QtCore.QRect(380, 80, 281, 151))
        self.frame_4.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.label_6 = QtGui.QLabel(self.frame_4)
        self.label_6.setGeometry(QtCore.QRect(20, 20, 54, 15))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.txtPlainLlave = QtGui.QTextEdit(self.frame_4)
        self.txtPlainLlave.setGeometry(QtCore.QRect(10, 50, 261, 91))
        self.txtPlainLlave.setObjectName(_fromUtf8("txtPlainLlave"))
        self.frame_5 = QtGui.QFrame(self.centralwidget)
        self.frame_5.setGeometry(QtCore.QRect(380, 240, 281, 311))
        self.frame_5.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.label_7 = QtGui.QLabel(self.frame_5)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.txtDireccionIPEsperaMensaje = QtGui.QLineEdit(self.frame_5)
        self.txtDireccionIPEsperaMensaje.setGeometry(QtCore.QRect(80, 30, 171, 23))
        self.txtDireccionIPEsperaMensaje.setObjectName(_fromUtf8("txtDireccionIPEsperaMensaje"))
        self.label_8 = QtGui.QLabel(self.frame_5)
        self.label_8.setGeometry(QtCore.QRect(10, 30, 81, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.label_9 = QtGui.QLabel(self.frame_5)
        self.label_9.setGeometry(QtCore.QRect(30, 60, 54, 15))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.txtPuertoEsperaMensaje = QtGui.QLineEdit(self.frame_5)
        self.txtPuertoEsperaMensaje.setGeometry(QtCore.QRect(80, 60, 171, 23))
        self.txtPuertoEsperaMensaje.setObjectName(_fromUtf8("txtPuertoEsperaMensaje"))
        self.btnConectarseEsperaMensaje = QtGui.QPushButton(self.frame_5)
        self.btnConectarseEsperaMensaje.setGeometry(QtCore.QRect(60, 90, 91, 24))
        self.btnConectarseEsperaMensaje.setObjectName(_fromUtf8("btnConectarseEsperaMensaje"))
        self.rbtnConectadoParaMensaje = QtGui.QRadioButton(self.frame_5)
        self.rbtnConectadoParaMensaje.setGeometry(QtCore.QRect(170, 90, 95, 21))
        self.rbtnConectadoParaMensaje.setText(_fromUtf8(""))
        self.rbtnConectadoParaMensaje.setObjectName(_fromUtf8("rbtnConectadoParaMensaje"))
        self.txtMensajeDesencriptado = QtGui.QTextEdit(self.frame_5)
        self.txtMensajeDesencriptado.setGeometry(QtCore.QRect(20, 160, 241, 131))
        self.txtMensajeDesencriptado.setObjectName(_fromUtf8("txtMensajeDesencriptado"))
        self.label_10 = QtGui.QLabel(self.frame_5)
        self.label_10.setGeometry(QtCore.QRect(20, 140, 171, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.lblStatus = QtGui.QLabel(self.centralwidget)
        self.lblStatus.setGeometry(QtCore.QRect(50, 560, 601, 16))
        self.lblStatus.setObjectName(_fromUtf8("lblStatus"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 690, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Empresa", None))
        self.label.setText(_translate("MainWindow", "Dirección IP", None))
        self.label_2.setText(_translate("MainWindow", "Puerto:", None))
        self.label_3.setText(_translate("MainWindow", "Nombre de org. :", None))
        self.btnEnviarDatosOrganizacion.setText(_translate("MainWindow", "Enviar", None))
        self.rbtnLlavePrivada.setText(_translate("MainWindow", "Llave Privada", None))
        self.rbtnLlavePublica.setText(_translate("MainWindow", "Llave Publica", None))
        self.btnSolicitarLlave.setText(_translate("MainWindow", "Solicitar Llave", None))
        self.label_4.setText(_translate("MainWindow", "Llave encriptada", None))
        self.label_5.setText(_translate("MainWindow", "Clave:", None))
        self.btnDesencriptarLlave.setText(_translate("MainWindow", "Desencriptar", None))
        self.label_6.setText(_translate("MainWindow", "Llave:", None))
        self.label_7.setText(_translate("MainWindow", "Esperar mensaje:", None))
        self.label_8.setText(_translate("MainWindow", "Dirección IP", None))
        self.label_9.setText(_translate("MainWindow", "Puerto:", None))
        self.btnConectarseEsperaMensaje.setText(_translate("MainWindow", "Conectarse", None))
        self.label_10.setText(_translate("MainWindow", "Mensaje desencriptado:", None))
        self.lblStatus.setText(_translate("MainWindow", "TextLabel", None))


    def start_request_to_info(self):
        start_new_thread(send_org_info, (self,))
        print  "Request started"

    def start_keys_request(self):
        start_new_thread(request_key, (self,))
        print "Started Request for the key"

    def set_key(self):
        self.txtLlaveEncriptada.setText(self.my_private_key)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
