from PyQt5.QtWidgets import *
import sqlite3
import main
from PyQt5.uic import loadUiType
login,_ = loadUiType('Login.ui')
class Login(QWidget,login):
    def __init__(self):       #constructor
        QWidget.__init__(self)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.Handel_Login)
    def Handel_Login(self):
        username=self.lineEdit.text()
        password=self.lineEdit_2.text()
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        username=self.lineEdit.text()
        password=self.lineEdit_2.text()
        self.cur.execute("SELECT * FROM USER")
        data = self.cur.fetchall()
        for row in data:
            if username==row[0] and password==row[2]:
                self.window2=main.MainApp()
                self.close()
                self.window2.show()
            else:
                self.label.setText("Incorrect UserName or Password")
