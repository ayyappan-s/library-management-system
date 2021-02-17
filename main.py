from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from xlrd import *
from xlsxwriter import *
import xlsxwriter
import sys
import sqlite3
import datetime
import login
import resources

from PyQt5.uic import loadUiType
ui,_ = loadUiType('library.ui')




class MainApp(QMainWindow, ui):
    def __init__(self):       #constructor
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_Ui_Changes()
        self.Handel_Buttons()
        self.database_connector()
        self.Show_Author()
        self.Show_Category()
        self.Show_Publisher()
        self.Show_Category_CB()
        self.Show_Author_CB()
        self.Show_Publisher_CB()
        self.Show_all_Client()
        self.Show_all_books()
        self.Show_all_Operations()
        self.title = 'SaiTech Softwares'
        self.setWindowTitle(self.title)


        self.comboBox_6.currentIndexChanged.connect(self.on_combobox_changed)

    def  on_combobox_changed(self):
        settings=self.comboBox_6.currentIndex()
        print("changes executed",settings)
        if settings==0:
            self.label_39.setText("Author name")
            self.label_40.setText("Author name")
            self.label_34.setText("Author Code")
        elif settings==1:
            self.label_40.setText("Publisher name")
            self.label_39.setText("Publisher name")
            self.label_34.setText("Publisher Code")
        elif settings==2:
            self.label_40.setText("Category name")
            self.label_39.setText("Category name")
            self.label_34.setText("Category Code")
    def Handel_Buttons(self):
            self.pushButton_5.clicked.connect(self.Show_themes)
            self.pushButton_31.clicked.connect(self.Hiding_Themes)
            self.pushButton.clicked.connect(self.Open_Day_To_Day_Tab)
            self.pushButton_2.clicked.connect(self.Open_Books_Tab)
            self.pushButton_14.clicked.connect(self.Open_Users_Tab)
            self.pushButton_4.clicked.connect(self.Open_Settings_Tab)
            self.pushButton_7.clicked.connect(self.Add_New_Book)
            self.pushButton_16.clicked.connect(self.Add_Category)
            self.pushButton_17.clicked.connect(self.Add_Author)
            self.pushButton_18.clicked.connect(self.Add_Publisher)
            self.pushButton_10.clicked.connect(self.Search_Book)
            self.pushButton_9.clicked.connect(self.Edit_Books)
            self.pushButton_11.clicked.connect(self.Delete_Books)
            self.pushButton_12.clicked.connect(self.Add_New_Users)
            self.pushButton_13.clicked.connect(self.Login)
            self.pushButton_15.clicked.connect(self.Edit_Users)
            self.pushButton_27.clicked.connect(self.dark_gray_theme)
            self.pushButton_28.clicked.connect(self.dark_blue_theme)
            self.pushButton_29.clicked.connect(self.dark_orange_theme)
            self.pushButton_30.clicked.connect(self.Qdark_theme)
            self.pushButton_8.clicked.connect(self.Open_Clients_Tab)
            self.pushButton_19.clicked.connect(self.Add_New_Client)
            self.pushButton_21.clicked.connect(self.Search_Client)
            self.pushButton_20.clicked.connect(self.Edit_Client)
            self.pushButton_22.clicked.connect(self.Delete_Client)
            self.pushButton_6.clicked.connect(self.Handel_Day_operations)
            self.pushButton_23.clicked.connect(self.Export_Day_Operations)
            self.pushButton_24.clicked.connect(self.Export_Clients)
            self.pushButton_25.clicked.connect(self.Export_Books)
            self.pushButton_3.clicked.connect(self.Theme_Reset)
            self.pushButton_32.clicked.connect(self.Delete)
            self.pushButton_33.clicked.connect(self.Search_Settings)
            self.pushButton_26.clicked.connect(self.Settings_Update)

    def Export_Clients(self):
        try:
            self.label_56.setText("")
            self.db = sqlite3.connect("library.db")
            self.cur = self.db.cursor()
            self.cur.execute("SELECT * FROM CLIENT")
            data = self.cur.fetchall()
            wb = Workbook("Clients.xlsx")
            sheet1 = wb.add_worksheet()
            sheet1.write(0, 0, 'Client Name')
            sheet1.write(0, 1, 'Client Email')
            sheet1.write(0, 2, 'National ID')
            row_number = 1
            for row in data:
                column_number = 0
                for item in row:
                    sheet1.write(row_number, column_number, str(item))
                    column_number += 1
                row_number += 1
            wb.close()
        except xlsxwriter.exceptions.FileCreateError:
            self.label_56.setText("Close The File & Try Again")

    def Search_Settings(self):
        settings=self.comboBox_6.currentText()
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        name=self.lineEdit_35.text()
        if settings=="Author":
            self.cur.execute("SELECT * FROM AUTHOR WHERE AUTHOR_NAME=?",(name,))
            data = self.cur.fetchall()
            for item in data:
                self.lineEdit_36.setText(item[1])
                self.lineEdit_21.setText(item[0])
        elif settings=="Category":
            self.cur.execute("SELECT * FROM CATEGORY WHERE CATEGORY_NAME=?",(name,))
            data = self.cur.fetchall()
            for item in data:
                self.lineEdit_36.setText(item[1])
                self.lineEdit_21.setText(item[0])
        else:
            self.cur.execute("SELECT * FROM PUBLISHER WHERE PUBLISHER_NAME=?",(name,))
            data = self.cur.fetchall()
            for item in data:
                self.lineEdit_36.setText(item[1])
                self.lineEdit_21.setText(item[0])


    def Delete(self):
        settings=self.comboBox_6.currentText()
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        name=self.lineEdit_35.text()
        code=self.lineEdit_21.text()
        if settings=="Author":
            self.cur.execute("DELETE FROM Author WHERE AUTHOR_NAME=?",(name,))
        if settings=="Publisher":
            self.cur.execute("DELETE FROM PUBLISHER WHERE PUBLISHER_NAME=?",(name,))
        if settings=="Category":
            self.cur.execute("DELETE FROM CATEGORY WHERE CATEGORY_NAME=?",(name,))
        self.statusBar().showMessage("Deleted Successfully")
        self.db.commit()
        self.cur.close()
        self.db.close()
        self.lineEdit_35.setText("")
        self.lineEdit_36.setText("")
        self.lineEdit_21.setText("")
    def Settings_Update(self):
        settings=self.comboBox_6.currentText()
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        S_name=self.lineEdit_35.text()
        name=self.lineEdit_36.text()
        code=self.lineEdit_21.text()
        if settings=="Author":
            self.cur.execute('''UPDATE  AUTHOR SET AUTHOR_NAME=?,AUTHOR_CODE=? WHERE AUTHOR_NAME=?''',(name,code,S_name,))
            self.db.commit()
            self.Show_Author()
            self.Show_Author_CB()
            print("authorExecuted",name,S_name,code)
        elif settings=="Publisher":
            self.cur.execute('''UPDATE  PUBLISHER SET PUBLISHER_NAME=?,PUBLISHER_CODE=? WHERE PUBLISHER_NAME=?''',(name,code,S_name,))
            self.db.commit()
            self.Show_Publisher()
            self.Show_Publisher_CB()
            print("Executed")
            print("publisherExecuted",name,S_name,code)
        elif settings=="Category":
            self.cur.execute('''UPDATE CATEGORY SET CATEGORY_NAME=?,CATEGORY_CODE=? WHERE CATEGORY_NAME=?''',(name,code,S_name,))
            self.db.commit()
            self.Show_Category()
            self.Show_Category_CB()
            print("Executed")
            print("categoryExecuted",name,S_name,code)
        self.statusBar().showMessage("Settings Updated")
        self.cur.close()
        self.db.commit()
        self.lineEdit_35.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_36.setText("")



##----------Day To Day Operations---------------#

    def Handel_Day_operations(self):

        book_title=self.lineEdit.text()
        client_name=self.lineEdit_20.text()
        if (book_title=="" or client_name==""):

                self.label_36.setText("Enter Book Title")
                self.label_48.setText("Enter Client Name")



        else:
            self.label_36.setText("")
            self.label_48.setText("")
            type=self.comboBox.currentText()
            day=self.comboBox_2.currentText()
            self.db=sqlite3.connect("library.db")
            self.cur=self.db.cursor()
            dat=datetime.date.today()
            if type=="Retrieve":
                day="Book Retrieved"
                dt="Book Retrieved"
                dat="Retrieved on " +str(dat)
            else:
                dt=datetime.datetime.today()+datetime.timedelta(days=int(day))
            self.label_36.setText("")
            self.label_48.setText("")
            self.cur.execute('''INSERT INTO DAY_TO_DAY(BOOK_NAME,CLIENT_NAME,TYPE,DAYS,DATE,TODAY) VALUES(?,?,?,?,?,?)''',
            (book_title,client_name,type,day,dat,dt))
            self.db.commit()
            self.cur.close()
            self.db.close()
            self.lineEdit.setText("")
            self.lineEdit_20.setText("")
            self.comboBox_2.setCurrentIndex(0)
            self.comboBox.setCurrentIndex(0)
            self.statusBar().showMessage("Activity Added")
            self.Show_all_Operations()
            book_title==""
            client_name=""
    def Show_all_Operations(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        self.cur.execute("SELECT * FROM DAY_TO_DAY")
        data=self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        for row ,operation in enumerate(data):
            for column ,dat in enumerate(operation):
                self.tableWidget.setItem(row,column,QTableWidgetItem(str(dat)))
                column=column+1
            row_pos=self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_pos)
            row=row+1

#-----------handling Functions-------------------#
    def Handel_Ui_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)

#--------------------Themes Handling Function-----------------------#
    def Show_themes(self):
        self.groupBox_6.show()
    def Hiding_Themes(self):
        self.groupBox_6.hide()
    def dark_blue_theme(self):
        style=open('themes/darkblue.css')
        style=style.read()
        self.setStyleSheet(style)
    def dark_gray_theme(self):
        style=open('themes/darkgray.css')
        style=style.read()
        self.setStyleSheet(style)
    def dark_orange_theme(self):
        style=open('themes/darkorange.css')
        style=style.read()
        self.setStyleSheet(style)
    def Qdark_theme(self):
        style=open('themes/qdark.css')
        style=style.read()
        self.setStyleSheet(style)
    def Theme_Reset(self):
        self.setStyleSheet("")
#-----------------Button Handling Functions-------------------------#
    def Open_Day_To_Day_Tab(self):
        self.tabWidget.setCurrentIndex(0)
    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(3)
    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(4)
    def Open_Clients_Tab(self):
        self.tabWidget.setCurrentIndex(2)
#################------Books------##################
    def Add_New_Book(self):
        try:
            self.label_49.setText("")
            self.db=sqlite3.connect("library.db")
            self.cur=self.db.cursor()
            book_title=self.lineEdit_3.text()
            book_description=self.textEdit_2.toPlainText()
            book_code=self.lineEdit_2.text()
            book_price=self.lineEdit_4.text()
            book_category=self.comboBox_3.currentText()
            book_author=self.comboBox_4.currentText()
            book_publisher=self.comboBox_5.currentText()
            self.cur.execute('''INSERT INTO BOOK(BOOK_TITLE,BOOK_CODE,BOOK_DESCRIPTION,BOOK_PRICE,BOOK_CATEGORY,BOOK_AUTHOR,BOOK_PUBLISHER) VALUES(?,?,?,?,?,?,?)
            ''',(book_title,book_code,book_description,book_price,book_category,book_author,book_publisher))
            self.db.commit()
            self.cur.close()
            self.db.close()
            self.statusBar().showMessage("New Book Added")
            self.comboBox_5.setCurrentIndex(0)
            self.comboBox_3.setCurrentIndex(0)
            self.comboBox_4.setCurrentIndex(0)
            self.lineEdit_4.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.textEdit_2.setPlainText('')
            self.Show_all_books()
        except sqlite3.IntegrityError:
            self.label_49.setText("Book Code is Already Available")

    def Search_Book(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        book_title=self.lineEdit_8.text()
        self.cur.execute("SELECT * FROM BOOK WHERE BOOK_TITLE=?",(book_title,))
        data=self.cur.fetchone()
        self.lineEdit_11.setText(data[0])
        self.lineEdit_9.setText(data[1])
        self.textEdit.setPlainText(data[2])
        index = self.comboBox_10.findText(data[3],Qt.MatchFixedString)
        self.comboBox_10.setCurrentIndex(index)
        index_2 = self.comboBox_11.findText(data[4],Qt.MatchFixedString)
        self.comboBox_11.setCurrentIndex(index_2)
        index_3 = self.comboBox_9.findText(data[5],Qt.MatchFixedString)
        self.comboBox_9.setCurrentIndex(index_3)
        self.lineEdit_10.setText(data[6])

    def Edit_Books(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        book_title=self.lineEdit_11.text()
        book_description=self.textEdit.toPlainText()
        book_code=self.lineEdit_9.text()
        book_price=self.lineEdit_10.text()
        book_category=self.comboBox_10.currentText()
        book_author=self.comboBox_11.currentText()
        book_publisher=self.comboBox_9.currentText()
        search_book_title=self.lineEdit_8.text()
        self.cur.execute('''UPDATE BOOK SET BOOK_TITLE=?,BOOK_DESCRIPTION=?,BOOK_CODE=?,BOOK_CATEGORY=?,BOOK_AUTHOR=?,BOOK_PUBLISHER=?,BOOK_PRICE=? WHERE BOOK_TITLE=?
        ''',(book_title,book_description,book_code,book_category,book_author,book_publisher,book_price,search_book_title))
        self.db.commit()
        self.cur.close()
        self.db.close()
        self.statusBar().showMessage("Book Updated")
        self.Show_all_books()

    def Delete_Books(self):
        warning=QMessageBox.warning(self,"Delete Book","are you sure you want to delete this book",QMessageBox.Yes | QMessageBox.No)
        if warning==QMessageBox.Yes:
                    self.db=sqlite3.connect("library.db")
                    self.cur=self.db.cursor()
                    del_title=self.lineEdit_8.text()
                    self.cur.execute("DELETE FROM BOOK WHERE BOOK_TITLE=?",(del_title,))
                    self.db.commit()
                    self.cur.close()
                    self.db.close()
                    self.statusBar().showMessage("Book Deleted")
                    self.Show_all_books()
                    book_title=self.lineEdit_11.setText("")
                    book_description=self.textEdit.setText("")
                    book_code=self.lineEdit_9.setText("")
                    book_price=self.lineEdit_10.setText("")
                    book_category=self.comboBox_10.setCurrentIndex(0)
                    book_author=self.comboBox_11.setCurrentIndex(0)
                    book_publisher=self.comboBox_9.setCurrentIndex(0)
                    search_book_title=self.lineEdit_8.setText("")
    def Show_all_books(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        self.cur.execute("SELECT * FROM BOOK")
        data=self.cur.fetchall()
        header = self.tableWidget_6.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)
        for row, book in enumerate(data):
            for column, item in enumerate(book):
                self.tableWidget_6.setItem(row,column,QTableWidgetItem(str(item)))
                column=column+1
            row_pos=self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_pos)
        self.db.commit()
        self.cur.close()
        self.db.close()

#########################-------Users-------##########################
    def Add_New_Users(self):
        try:
            self.label_50.setText("")
            self.db=sqlite3.connect("library.db")
            self.cur=self.db.cursor()
            usr_name=self.lineEdit_12.text()
            usr_email=self.lineEdit_13.text()
            usr_pass=self.lineEdit_14.text()
            pass_again=self.lineEdit_15.text()
            if usr_pass==pass_again:
                self.cur.execute("INSERT INTO USER(USER_NAME,USER_EMAIL,USER_PASS) VALUES(?,?,?)",(usr_name,usr_email,usr_pass))
                self.db.commit()
                self.cur.close()
                self.db.close()
                self.statusBar().showMessage("User Added")
                usr_name=self.lineEdit_12.setText("")
                usr_email=self.lineEdit_13.setText("")
                usr_pass=self.lineEdit_14.setText("")
                pass_again=self.lineEdit_15.setText("")
            else:
                self.label_12.setText('Please add a valid password twice')
        except sqlite3.IntegrityError:
            self.label_50.setText("UserName Already Exists")

    def Login(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        usr_name=self.lineEdit_16.text()
        usr_pass=self.lineEdit_18.text()
        self.cur.execute("SELECT * FROM USER")
        data = self.cur.fetchall()
        for row in data:
            if usr_name==row[0] and usr_pass==row[2]:
                self.statusBar().showMessage("Valid Username & Password")
                self.groupBox_4.setEnabled(True)
                self.lineEdit_24.setText(row[0])
                self.lineEdit_17.setText(row[1])
                self.lineEdit_25.setText(row[2])
                self.lineEdit_19.setText(row[2])

    def Edit_Users(self):
        try:
            self.label_54.setText("")
            login_name=self.lineEdit_16.text()
            user_name=self.lineEdit_24.text()
            user_email=self.lineEdit_17.text()
            user_pass=self.lineEdit_25.text()
            user_pass_again=self.lineEdit_19.text()
            if user_pass==user_pass_again:
                        self.db=sqlite3.connect("library.db")
                        self.cur=self.db.cursor()
                        self.cur.execute(''' UPDATE USER SET USER_NAME=?,USER_EMAIL=?,USER_PASS=? WHERE USER_NAME=?
                        ''',(user_name,user_email,user_pass,login_name))
                        self.db.commit()
                        self.cur.close()
                        self.db.close()
                        self.statusBar().showMessage("User Data Updated")
                        usr_name=self.lineEdit_16.setText("")
                        usr_pass=self.lineEdit_18.setText("")
                        user_name=self.lineEdit_24.setText("")
                        user_email=self.lineEdit_17.setText("")
                        user_pass=self.lineEdit_25.setText("")
                        user_pass_again=self.lineEdit_19.setText("")
            else:
                self.label_13.setText("Password Does Not Match")
        except sqlite3.IntegrityError:
            self.label_54.setText("User Name Already Exists")
#########################-------Clients-------##########################
    def Add_New_Client(self):
        client_name=self.lineEdit_23.text()
        client_email=self.lineEdit_29.text()
        client_id=self.lineEdit_30.text()
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        self.cur.execute('''INSERT INTO CLIENT(CLIENT_NAME,CLIENT_ID,CLIENT_EMAIL) VALUES(?,?,?)
        ''',(client_name,client_id,client_email))
        self.db.commit()
        self.cur.close()
        self.db.close()
        self.statusBar().showMessage("Client Details Added")
        self.Show_all_Client()
        client_name=self.lineEdit_23.setText("")
        client_email=self.lineEdit_29.setText("")
        client_id=self.lineEdit_30.setText("")


    def Show_all_Client(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        self.cur.execute("SELECT * FROM CLIENT")
        data=self.cur.fetchall()
        header = self.tableWidget_5.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)
        for row, client in enumerate(data):
            for column, item in enumerate(client):
                self.tableWidget_5.setItem(row,column,QTableWidgetItem(str(item)))
                column=column+1
            row_pos=self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_pos)
        self.db.commit()
        self.cur.close()
        self.db.close()


    def Search_Client(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        CLIENT_NAME=self.lineEdit_31.text()
        self.cur.execute(''' SELECT * FROM CLIENT WHERE CLIENT_NAME=?''',(CLIENT_NAME,))
        data=self.cur.fetchall()
        for row in data:
            if row[0]==CLIENT_NAME:
                self.lineEdit_32.setText(row[0])
                self.lineEdit_34.setText(row[1])
                self.lineEdit_33.setText(row[2])
        self.db.commit()
        self.cur.close()
        self.db.close()

    def Edit_Client(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        S_CLIENT_NAME=self.lineEdit_31.text()
        client_name=self.lineEdit_32.text()
        client_email=self.lineEdit_34.text()
        client_id=self.lineEdit_33.text()
        self.cur.execute('''UPDATE CLIENT SET CLIENT_NAME=?,CLIENT_ID=?,CLIENT_EMAIL=?
        WHERE CLIENT_NAME=?''',(client_name,client_id,client_email,S_CLIENT_NAME))
        self.db.commit()
        self.cur.close()
        self.db.close()
        self.statusBar().showMessage("Client Details Updated")
        self.lineEdit_31.setText('')
        self.lineEdit_32.setText('')
        self.lineEdit_34.setText('')
        self.lineEdit_33.setText('')
        self.Show_all_Client()
    def Delete_Client(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        S_CLIENT_NAME=self.lineEdit_31.text()
        if S_CLIENT_NAME==None:
            self.label_33.setText("Enter Client Name")
        self.cur.execute("DELETE FROM CLIENT WHERE CLIENT_NAME=?",(S_CLIENT_NAME,))
        self.db.commit()
        self.cur.close()
        self.db.close()
        self.statusBar().showMessage("Client Details Deleted")
        self.lineEdit_31.setText('')
        self.lineEdit_32.setText('')
        self.lineEdit_34.setText('')
        self.lineEdit_33.setText('')
        self.Show_all_Client()


















    ############------Category-----#########################
    def Add_Category(self):
        try:
            self.label_51.setText("")
            self.db=sqlite3.connect("library.db")
            self.cur=self.db.cursor()
            category_name=self.lineEdit_26.text()
            category_code=self.lineEdit_5.text()
            self.cur.execute("INSERT INTO CATEGORY (CATEGORY_CODE,CATEGORY_NAME) VALUES(?,?)",(category_code,category_name,))
            self.db.commit()
            self.cur.close()
            self.db.close()
            self.statusBar().showMessage("New Category Added")
            self.lineEdit_26.setText('')
            self.lineEdit_5.setText('')
            self.Show_Category()
            self.Show_Category_CB()
        except sqlite3.IntegrityError:
            self.label_51.setText("Category Code Already Exists")
    def Show_Category(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        self.cur.execute('SELECT * FROM CATEGORY')
        data = self.cur.fetchall()
        header = self.tableWidget_2.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        col=0
        self.tableWidget_2.setRowCount(len(data))
        self.tableWidget_2.setColumnCount(2)
        if data:
            for row,category in enumerate(data):
                 for col in range(0,2):
                       if col==0:
                           self.tableWidget_2.setItem(row,col,QTableWidgetItem(category[0]))
                       if col==1:
                           self.tableWidget_2.setItem(row,col,QTableWidgetItem(category[1]))
        self.db.close()

    def Add_Author(self):
        try:
            self.label_52.setText("")
            self.db=sqlite3.connect("library.db")
            self.cur=self.db.cursor()
            author_name=self.lineEdit_27.text()
            author_code=self.lineEdit_6.text()
            self.cur.execute("INSERT INTO AUTHOR (AUTHOR_CODE,AUTHOR_NAME) VALUES(?,?)",(author_code,author_name,))
            self.db.commit()
            self.cur.close()
            self.db.close()
            self.statusBar().showMessage("New Author Added")
            self.lineEdit_27.setText('')
            self.lineEdit_6.setText('')
            self.Show_Author()
            self.Show_Author_CB()
        except sqlite3.IntegrityError:
            self.label_52.setText("Author Code Already Exists")
    def Show_Author(self):
        self.db=sqlite3.connect("library.db")
        self.cur=self.db.cursor()
        self.cur.execute('SELECT * FROM AUTHOR')
        data = self.cur.fetchall()
        col=0
        header = self.tableWidget_3.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.tableWidget_3.setRowCount(len(data))
        self.tableWidget_3.setColumnCount(2)
        if data:
            for row,author in enumerate(data):
                for col in range(0,2):
                       if col==0:
                           self.tableWidget_3.setItem(row,col,QTableWidgetItem(author[0]))
                       if col==1:
                           self.tableWidget_3.setItem(row,col,QTableWidgetItem(author[1]))

    def database_connector(self):
        self.db = sqlite3.connect("library.db")
        self.c = self.db.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS CATEGORY
           (CATEGORY_CODE NOT NULL PRIMARY KEY,CATEGORY_NAME TEXT NOT NULL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS AUTHOR
           (AUTHOR_CODE NOT NULL PRIMARY KEY,AUTHOR_NAME TEXT NOT NULL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS PUBLISHER
           (PUBLISHER_CODE NOT NULL PRIMARY KEY,PUBLISHER_NAME TEXT NOT NULL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS BOOK(BOOK_TITLE NOT NULL,BOOK_CODE
           NOT NULL PRIMARY KEY, BOOK_DESCRIPTION NOT NULL,
           BOOK_CATEGORY NOT NULL,BOOK_AUTHOR NOT NULL,BOOK_PUBLISHER NOT NULL, BOOK_PRICE NOT NULL)
           ''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS USER(USER_NAME NOT NULL PRIMARY KEY,
           USER_EMAIL NOT NULL,USER_PASS NOT NULL)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS CLIENT(CLIENT_NAME NOT NULL,
           CLIENT_EMAIL NOT NULL ,CLIENT_ID NOT NULL PRIMARY KEY)''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS DAY_TO_DAY(BOOK_NAME NOT NULL,
           CLIENT_NAME TEXT, TYPE NOT NULL, DAYS DATE, DATE NOT NULL ,TODAY DATE)''')
        self.db.commit()
        self.c.close()
        self.db.close()
    def Add_Publisher(self):
        try:
            self.label_53.setText("")
            self.db=sqlite3.connect("library.db")
            self.cur=self.db.cursor()
            publisher_name=self.lineEdit_28.text()
            publisher_code=self.lineEdit_7.text()
            self.cur.execute("INSERT INTO PUBLISHER (PUBLISHER_CODE,PUBLISHER_NAME) VALUES(?,?)",(publisher_code,publisher_name,))
            self.db.commit()
            self.cur.close()
            self.db.close()
            self.statusBar().showMessage("New Publisher Added")
            self.lineEdit_28.setText('')
            self.lineEdit_7.setText('')
            self.Show_Publisher()
            self.Show_Publisher_CB()
        except sqlite3.IntegrityError:
            self.label_53.setText("Publisher Code Already Exists")
    def Show_Publisher(self):
            self.db=sqlite3.connect("library.db")
            self.cur=self.db.cursor()
            self.cur.execute('SELECT * FROM PUBLISHER')
            data = self.cur.fetchall()
            header = self.tableWidget_4.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
            col=0
            self.tableWidget_4.setRowCount(len(data))
            self.tableWidget_4.setColumnCount(2)
            if data:
                for row,publisher in enumerate(data):
                    for col in range(0,2):
                           if col==0:
                               self.tableWidget_4.setItem(row,col,QTableWidgetItem(publisher[0]))
                           if col==1:
                               self.tableWidget_4.setItem(row,col,QTableWidgetItem(publisher[1]))

    def Show_Category_CB(self):
        self.db=sqlite3.connect("library.db")
        self.c=self.db.cursor()
        self.c.execute("SELECT CATEGORY_NAME FROM CATEGORY")
        data=self.c.fetchall()
        self.comboBox_10.clear()
        self.comboBox_3.clear()
        for items in data:
            self.comboBox_10.addItems(items)
            self.comboBox_3.addItems(items)
    def Show_Author_CB(self):
        self.db=sqlite3.connect("library.db")
        self.c=self.db.cursor()
        self.c.execute("SELECT AUTHOR_NAME FROM AUTHOR")
        data=self.c.fetchall()
        self.comboBox_11.clear()
        self.comboBox_4.clear()
        for items in data:
            self.comboBox_11.addItems(items)
            self.comboBox_4.addItems(items)
    def Show_Publisher_CB(self):
        self.db=sqlite3.connect("library.db")
        self.c=self.db.cursor()
        self.c.execute("SELECT PUBLISHER_NAME FROM PUBLISHER")
        data=self.c.fetchall()
        self.comboBox_9.clear()
        self.comboBox_5.clear()
        for items in data:
            self.comboBox_9.addItems(items)
            self.comboBox_5.addItems(items)
#######-----Exporting Data-----#########
    def Export_Day_Operations(self):
        try:
           self.label_55.setText("")
           self.db=sqlite3.connect("library.db")
           self.cur=self.db.cursor()
           self.cur.execute("SELECT * FROM DAY_TO_DAY")
           data=self.cur.fetchall()
           wb=Workbook("day_operations.xlsx")
           sheet1=wb.add_worksheet()
           sheet1.write(0,0,'Book Name')
           sheet1.write(0,1,'Client Name')
           sheet1.write(0,2,'Type')
           sheet1.write(0,3,'Days ')
           sheet1.write(0,4,'From')
           sheet1.write(0,5,'Till')
           row_number=1
           for row in data:
               column_number=0
               for item in row:
                   sheet1.write(row_number,column_number,str(item))
                   column_number+=1
               row_number+=1
           wb.close()
        except xlsxwriter.exceptions.FileCreateError:
           self.label_55.setText("Close The File & Try Again")

    def Export_Books(self):
        try:
           self.label_57.setText("")
           self.db=sqlite3.connect("library.db")
           self.cur=self.db.cursor()
           self.cur.execute("SELECT * FROM BOOK")
           data=self.cur.fetchall()
           wb=Workbook("Books.xlsx")
           sheet1=wb.add_worksheet()
           sheet1.write(0,0,'Book Name')
           sheet1.write(0,1,'Book Code')
           sheet1.write(0,2,'Book Description')
           sheet1.write(0,3,'Book Category')
           sheet1.write(0,4,'Book Author')
           sheet1.write(0,5,'Book Publisher')
           sheet1.write(0,6,'Book Price')
           row_number=1
           for row in data:
                column_number=0
                for item in row:
                    sheet1.write(row_number,column_number,str(item))
                    column_number+=1
                row_number+=1
           wb.close()
        except xlsxwriter.exceptions.FileCreateError:
           self.label_57.setText("Close The File & Try Again")
    

def main():
    app = QApplication(sys.argv)
    db=sqlite3.connect("library.db")
    cur=db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USER(USER_NAME NOT NULL PRIMARY KEY,
    USER_EMAIL NOT NULL,USER_PASS NOT NULL)''')
    cur.execute("SELECT count(*) from USER")
    if cur.fetchone()[0]==1:
            window = login.Login()
            window.show()
            app.exec()
    else:
        window=MainApp()
        window.show()
        app.exec()
if __name__=="__main__":
    main()
