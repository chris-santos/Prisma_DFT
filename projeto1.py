# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'projeto1.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnFileFind = QtWidgets.QPushButton(self.centralwidget)
        self.btnFileFind.setGeometry(QtCore.QRect(70, 40, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnFileFind.setFont(font)
        self.btnFileFind.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.btnFileFind.setObjectName("btnFileFind")
        self.btnFileFind.clicked.connect(self.btn1_click)
        #
        self.fileName = ""
        self.lines = []
        self.vibfreqList = []
        
        self.btnCsvCreate = QtWidgets.QPushButton(self.centralwidget)
        self.btnCsvCreate.setGeometry(QtCore.QRect(70, 310, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnCsvCreate.setFont(font)
        self.btnCsvCreate.setStyleSheet("background-color: rgb(170, 170, 127);")
        self.btnCsvCreate.setObjectName("btnCsvCreate")
        self.lblInfo = QtWidgets.QLabel(self.centralwidget)
        self.lblInfo.setGeometry(QtCore.QRect(480, 10, 111, 31))
        font = QtGui.QFont()
        #font.setFamily("MS Serif")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblInfo.setFont(font)
        self.lblInfo.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"color: rgb(0, 85, 255);")
        self.lblInfo.setObjectName("lblInfo")
        self.lstFreq = QtWidgets.QListWidget(self.centralwidget)
        self.lstFreq.setGeometry(QtCore.QRect(290, 50, 461, 411))
        self.lstFreq.setObjectName("lstFreq")
        self.lblResult = QtWidgets.QLabel(self.centralwidget)
        self.lblResult.setGeometry(QtCore.QRect(290, 480, 491, 31))
        font = QtGui.QFont()
       #font.setFamily("MS Serif")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblResult.setFont(font)
        self.lblResult.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"color: rgb(0, 85, 255);")
        self.lblResult.setObjectName("lblResult")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Orca Output Parser"))
        self.btnFileFind.setText(_translate("MainWindow", "Abrir arquivo"))
        self.btnCsvCreate.setText(_translate("MainWindow", "Gerar csv"))
        self.lblInfo.setText(_translate("MainWindow", "INFORMAÇÕES"))
        self.lblResult.setText(_translate("MainWindow", "análise"))

    
    def parseFile(self):
        
        try:
            with open(self.fileName, 'rt') as outfile:
                #texto = outfile.read()
                for line in outfile:
                    if not line.isspace():
                        self.lines.append(line.rstrip("\n"))
            #find input
            input_str = 'INPUT FILE'
            input_end_str = 'END OF INPUT'
            input_start = 0
            input_end = 0

            for i in range(len(self.lines)):
                if input_str in self.lines[i]:
                    #print('input starts in line:' , i)
                    input_start = i
                if input_end_str in self.lines[i]:
                    input_end = i

            #for i in range(10):
            #    print(i, lines[input_start +3 + i])

            inpline = input_start + 2
            input_name = self.lines[inpline]
            #print(input_name)
            #print(lines[input_end])

            print('********  Seção INPUT: **************')
            for i in range(inpline,input_end):
                print(self.lines[i][6:])

            # FREQUENCIAS
            VIBRATIONAL_str = 'VIBRATIONAL FREQUENCIES'
            NORMAL_MODES_str = 'NORMAL MODES'
            vibr_start = 0
            vibr_end = 0

            for i in range(len(self.lines)):
                if VIBRATIONAL_str in self.lines[i]:
                    #print('input starts in line:' , i)
                    vibr_start = i
                if NORMAL_MODES_str in self.lines[i]:
                    vibr_end = i - 1
            #for i in range(10):
            #    print(i, lines[input_start +3 + i])

            for i in range(vibr_start + 4,vibr_end):
                dado = self.lines[i][6:].rstrip('cm**-1')
                self.vibfreqList.append(dado)
                self.lstFreq.addItem(dado)
                #print(lines[i][6:])
            
            negative_count = 0
            negativeFreq_list = []

            print('Frequencias (cm-¹):\n _____________________')

            for i in range(len(self.vibfreqList)):
                print(i, self.vibfreqList[i])
                if '-' in self.vibfreqList[i]:
                    negativeFreq_list.append(self.vibfreqList[i])

            if len(negativeFreq_list ) > 0:
                print("\nFrequências negativas (cm-¹):\n _____________________")
                for i in range (len(negativeFreq_list)):
                    print(negativeFreq_list[i])
            else:
                print("__________________________________________\nLucky guy!!! Não há frequências negativas.")

        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            print("xiii, zuou o baguio!")

    def checkFile(self):
        if self.fileName.isspace():
            print('metodo test-if: ', self.fileName)
            self.lblResult.setText("arquivo vazio.")            
        else:
            self.lblResult.setText(self.fileName)
            self.parseFile()
    
    def btn1_click(self):
        #print('o botão 1 foi clicado')
        self.btnFileFind.setStyleSheet('QPushButton {background-color:cyan; font:bold}')
        
        fileName = QFileDialog.getOpenFileName(self, "Open Output", "/orcafiles/new", "Orca Files (*.out *.txt)")
        self.fileName = fileName[0]
        print('metodo btn: ', self.fileName)
        #arquivo = QFileDialog.getOpenFileName(self,'Escolha o output', "Output (*.out);; Text files (*.txt);; All (*.*)")
        self.checkFile()
            
        #self.lblResult.setText(fileName[0])
        
        
    
        
            
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
