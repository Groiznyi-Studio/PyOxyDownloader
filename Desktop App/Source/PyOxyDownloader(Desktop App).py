# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import sys
import requests
import sys
import os.path as osp #os.path -> osp

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(320, 107)
        MainWindow.setMinimumSize(QtCore.QSize(320, 107))
        MainWindow.setMaximumSize(QtCore.QSize(320, 107))
        MainWindow.setStyleSheet("background-color: \n"
"#393e45\n"
"")
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 231, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setStyleSheet("color: #808b9c")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 0, 81, 20))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(153, 90, 171, 20))
        self.label_2.setObjectName("label_2")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(240, 20, 61, 21))
        self.pushButton.setStyleSheet("background-color: \n"
"#505761\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 60, 61, 21))
        self.pushButton_2.setStyleSheet("background-color: \n"
"#505761\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 60, 230, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setStyleSheet("color: #808b9c")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(110, 40, 81, 20))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "OxyDownloader - None", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Url Oxy.Cloud", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "OxyDownloader by Groiznyi-Studio", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("MainWindow", "Select", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Path To Save", None, QtGui.QApplication.UnicodeUTF8))
        

class Core():
    __Params = {
        "ActiveDirectory" : sys.argv[0][0:len(sys.argv[0]) - len(osp.basename(sys.argv[0])) - 1],
        "HtmlCodePage" : None,
        "MainUrl" : "",
        "SecondUrl" : "",
        "FinalUrl" : "",
        "NameFile" : ""}

    def GetHtmlCodePage(Url, Content = False):
        if Content == False:
            try:
                HtmlCodePage = requests.get(Url)
                Core.__Params["HtmlCodePage"] = HtmlCodePage.text
                return 1
            except:
                raise Core.CoreException("GetPage return error!!!")
            
        elif Content:
            try:
                HtmlCodePage = requests.get(Url)
                Core.__Params["HtmlCodePage"] = HtmlCodePage.content
                return 1
            except:
                raise Core.CoreException("GetPage return error!!!")
        else:
            return 0

    def SetParam(Param, Data):
        if Param in Core.__Params:
            Core.__Params[Param] = Data
        else:
            raise Core.CoreException("ClearParam \""+Param+"\" not defined!!!")
            
    def GetParam(Param):
        if Param in Core.__Params:
            return Core.__Params[Param]
        else:
            raise Core.CoreException("ClearParam \""+Param+"\" not defined!!!")
            
    def ClearParam(Param):
        if Param in Core.__Params:
            Core.__Params[Param] = None
            return 1
        else:
            raise Core.CoreException("ClearParam \""+Param+"\" not defined!!!")
            
    def GetNextUrl(Data, Step):
        if Step == 1:
            for Line in Data:
                if Line.find("  <a href=\"https:") != -1:
                     Core.__Params["SecondUrl"] = Line
                     break            
            Index = 11
            for char in Core.GetParam("SecondUrl")[11:len(Core.GetParam("SecondUrl"))]:
                Index += 1
                if char == "\"":
                    Core.__Params["SecondUrl"] = Core.GetParam("SecondUrl")[11:Index-1]
                    break
                
        elif Step == 2:
            for Line in Data:
                if Line.find("                                              var page_url = \'") != -1:
                     Core.__Params["FinalUrl"] = Line
                     break
            Index = 64
            for Char in Core.GetParam("FinalUrl")[64:len(Core.GetParam("FinalUrl"))]:
                Index += 1
                if Char == "\'":
                    Core.__Params["FinalUrl"] = Core.GetParam("FinalUrl")[64:Index-1]
                    Core.__Params["FinalUrl"] = "http://"+Core.GetParam("FinalUrl")
                    break

    def GetNameFile(Data):
        for Line in Data:
            if Line.find("                                              <b>Название файла:</b> ") != -1:
                 Core.__Params["NameFile"] = Line
                 break
        Index = 69
        for Char in Core.GetParam("NameFile")[69:len(Core.GetParam("NameFile"))]:
            Index += 1
            if Char == "<":
                Core.__Params["NameFile"] = Core.GetParam("NameFile")[69:Index-2]
                break
        
    def WriteHtmlCodePage(NameFile, Content = False):
        if Content == False:
            try:
                File = open(Core.__Params["ActiveDirectory"]+"/"+NameFile, "w")
                File.write(Core.__Params["HtmlCodePage"])
                File.close()
                return 1
            except:
                raise Core.CoreException("WriteFile return error!!!")
        elif Content:
            try:
                File = open(Core.__Params["ActiveDirectory"]+"/"+NameFile, "wb")
                File.write(Core.__Params["HtmlCodePage"])
                File.close()
                return 1
            except:
                raise Core.CoreException("WriteFile return error!!!")

    def DeleteFile(NameFile):
        try:
            os.remove(Core.__Params["ActiveDirectory"]+"/"+NameFile)
            return 1
        except:
            return 0
    
    class CoreException(Exception):
        def __init__(self, Message):
            self.Message = Message
            

global StatusChoosed
StatusChoosed = 0
        
def DownloadFile():
    if(StatusChoosed == 0):
        Root = tk.Tk()
        Root.withdraw()
        tk.messagebox.showerror(title="Error", message="Save folder cannot be empty!!!")
    else:
        if(ui.lineEdit.text() == ""):
            Root = tk.Tk()
            Root.withdraw()
            tk.messagebox.showerror(title="Error", message="Url cannot be empty!!!")
        else:
            try:
                tk.messagebox.showinfo(title="Info", message="Url: "+ui.lineEdit.text()+"\nSave To Folder: "+ui.lineEdit_2.text())
                #First Step
                Core.SetParam("ActiveDirectory", ui.lineEdit_2.text())
                Core.SetParam("MainUrl", ui.lineEdit.text())
                exec("MainWindow.setWindowTitle(\"OxyDownloader - GetPage_1\")")
                Core.GetHtmlCodePage(Core.GetParam("MainUrl"))
                exec("MainWindow.setWindowTitle(\"OxyDownloader - AnalyzingPage_1\")")
                Core.GetNextUrl(Core.GetParam("HtmlCodePage").split('\n'), 1)
                Core.ClearParam("HtmlCodePage")
                
                #Second Step
                exec("MainWindow.setWindowTitle(\"OxyDownloader - GetPage_2\")")
                Core.GetHtmlCodePage(Core.GetParam("SecondUrl"))
                exec("MainWindow.setWindowTitle(\"OxyDownloader - AnalyzingPage_2\")")
                Core.GetNextUrl(Core.GetParam("HtmlCodePage").split('\n'), 2)
                Core.GetNameFile(Core.GetParam("HtmlCodePage").split('\n'))
                Core.ClearParam("HtmlCodePage")

                #Final Step
                exec("MainWindow.setWindowTitle(\"OxyDownloader - GetPage_3\")")
                Core.GetHtmlCodePage(Core.GetParam("FinalUrl"), True)
                exec("MainWindow.setWindowTitle(\"OxyDownloader - Download: \"+\""+Core.GetParam("NameFile")+"\")")
                Core.WriteHtmlCodePage(Core.GetParam("NameFile"), True)
                exec("MainWindow.setWindowTitle(\"OxyDownloader - Finish\")")
                
            except Core.CoreException as CE:
                MainWindow.setWindowTitle("OxyDownloader - Error")
                Root = tk.Tk()
                Root.withdraw()
                tk.messagebox.showerror(title="ErrorDownload", message=CE)

                        
def SetActiveDirectory():
    Root = tk.Tk()
    Root.withdraw()
    ActiveDirectory = tk.filedialog.askdirectory(parent=Root,initialdir="/",title='Please select a directory')
    if ActiveDirectory == "":
        tk.messagebox.showerror(title="Error", message="You have not selected a folder!!!")
    else:
        global StatusChoosed
        StatusChoosed = 1
        ui.lineEdit_2.setText(ActiveDirectory)

        
app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)


ui.pushButton.clicked.connect(DownloadFile)
ui.pushButton_2.clicked.connect(SetActiveDirectory)


MainWindow.show()
sys.exit(app.exec_())
