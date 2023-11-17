# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'projeto1.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
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
        font.setFamily("MS Serif")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblInfo.setFont(font)
        self.lblInfo.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"color: rgb(0, 85, 255);")
        self.lblInfo.setObjectName("lblInfo")
        self.lblResult = QtWidgets.QLabel(self.centralwidget)
        self.lblResult.setGeometry(QtCore.QRect(290, 480, 491, 31))
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblResult.setFont(font)
        self.lblResult.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"color: rgb(0, 85, 255);")
        self.lblResult.setObjectName("lblResult")
        self.lstFreq = QtWidgets.QListWidget(self.centralwidget)
        self.lstFreq.setGeometry(QtCore.QRect(290, 50, 461, 411))
        self.lstFreq.setObjectName("lstFreq")
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
