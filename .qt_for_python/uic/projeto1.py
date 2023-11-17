# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Documentos\Python Scripts\QT UI\output\Prisma\projeto1.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(741, 600)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lstNegatives = QtWidgets.QListWidget(self.centralwidget)
        self.lstNegatives.setGeometry(QtCore.QRect(640, 170, 91, 251))
        self.lstNegatives.setObjectName("lstNegatives")
        self.txtFreqList = QtWidgets.QTextEdit(self.centralwidget)
        self.txtFreqList.setGeometry(QtCore.QRect(420, 170, 201, 351))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txtFreqList.setFont(font)
        self.txtFreqList.setReadOnly(True)
        self.txtFreqList.setObjectName("txtFreqList")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 0, 351, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnFileFind = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnFileFind.setFont(font)
        self.btnFileFind.setStyleSheet("background-color: rgb(0, 170, 255);")
        self.btnFileFind.setObjectName("btnFileFind")
        self.horizontalLayout.addWidget(self.btnFileFind)
        self.btnBatchJob = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.btnBatchJob.setFont(font)
        self.btnBatchJob.setAutoFillBackground(False)
        self.btnBatchJob.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.btnBatchJob.setObjectName("btnBatchJob")
        self.horizontalLayout.addWidget(self.btnBatchJob)
        self.btnInputCreator = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btnInputCreator.setStyleSheet("background-color: rgb(255, 170, 127);")
        self.btnInputCreator.setObjectName("btnInputCreator")
        self.horizontalLayout.addWidget(self.btnInputCreator)
        self.btnIRCreate = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnIRCreate.setFont(font)
        self.btnIRCreate.setStyleSheet("background-color: rgb(170, 170, 127);")
        self.btnIRCreate.setObjectName("btnIRCreate")
        self.horizontalLayout.addWidget(self.btnIRCreate)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(30, 90, 701, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblInfo = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.lblInfo.setFont(font)
        self.lblInfo.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 85, 255);")
        self.lblInfo.setAlignment(QtCore.Qt.AlignCenter)
        self.lblInfo.setObjectName("lblInfo")
        self.horizontalLayout_2.addWidget(self.lblInfo)
        self.lblResult = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("MS Serif")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblResult.setFont(font)
        self.lblResult.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"color: rgb(0, 85, 255);")
        self.lblResult.setAlignment(QtCore.Qt.AlignCenter)
        self.lblResult.setObjectName("lblResult")
        self.horizontalLayout_2.addWidget(self.lblResult)
        self.txtInput = QtWidgets.QTextEdit(self.centralwidget)
        self.txtInput.setGeometry(QtCore.QRect(30, 170, 361, 351))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.txtInput.setFont(font)
        self.txtInput.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.txtInput.setReadOnly(True)
        self.txtInput.setObjectName("txtInput")
        self.btnSobre = QtWidgets.QPushButton(self.centralwidget)
        self.btnSobre.setGeometry(QtCore.QRect(610, 0, 126, 24))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btnSobre.setFont(font)
        self.btnSobre.setStyleSheet("background-color: rgb(85, 255, 0);")
        self.btnSobre.setObjectName("btnSobre")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 741, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prisma - Quantum Calculation Tools"))
        self.btnFileFind.setToolTip(_translate("MainWindow", "escolha arquivo de output"))
        self.btnFileFind.setText(_translate("MainWindow", "Abrir arquivo"))
        self.btnBatchJob.setToolTip(_translate("MainWindow", "Defina a pasta inicial p/ gerar todos espectros"))
        self.btnBatchJob.setText(_translate("MainWindow", "BatchJob"))
        self.btnInputCreator.setText(_translate("MainWindow", "Gerar Input"))
        self.btnIRCreate.setToolTip(_translate("MainWindow", "gera o csv do espectro convoluído"))
        self.btnIRCreate.setText(_translate("MainWindow", "Gerar IR"))
        self.lblInfo.setText(_translate("MainWindow", "INFORMAÇÕES"))
        self.lblResult.setText(_translate("MainWindow", "Análise"))
        self.btnSobre.setToolTip(_translate("MainWindow", "informações"))
        self.btnSobre.setText(_translate("MainWindow", "Sobre"))
