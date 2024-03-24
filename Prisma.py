"""
Created on Mon October 10 10:00h 2020

@author: Christiano
    GUI para processar o arquivo de output do orca, gerar espectro, exportar dados
"""
from controller import Controller, DAO, InputGenerator
from dataLayer import DAO
# pip install pyqt5
from PyQt5 import QtWidgets, uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import sys
import os.path

# criar grafico IR
# pip install matplotlib
import matplotlib.pyplot as graph
import math

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('projeto1.ui', self)
        ### DATA LAYER
        self.controller = None
        self.dataObj = None
        
        ####    Variáveis de apoio        
        self.labelHeader = "Input Section"        
        self.dataLegend = "\n Wave number (cm-¹) | T**2 (km/mol) "
        self.msgFrequenciaNegativa = "Oops! Frequências negativas! " + self.dataLegend           
        self.vibfreqList = []
        self.irData = []
        self.negativeFreq_list = []
        self.copia = ''      
        self.pastaInput = ''  
        self.pastaOutput = ''

    ####    encontrar os elementos
        self.btnAbrir = self.findChild(QtWidgets.QPushButton, 'btnFileFind')
        self.btnAbrir.clicked.connect(self.btnAbrir_click)
        #gerar espectros em lote
        self.btnBatchJob = self.findChild(QtWidgets.QPushButton, 'btnBatchJob')
        self.btnBatchJob.clicked.connect(self.btnBatchJob_click)
        #btnIRCreate
        self.btnIRCreate = self.findChild(QtWidgets.QPushButton, 'btnIRCreate')
        self.btnIRCreate.clicked.connect(self.btnIR_click)
        #gerar input
        self.btnInputCreate = self.findChild(QtWidgets.QPushButton, 'btnInputCreator')
        self.btnInputCreate.clicked.connect(self.btnInput_click)

        self.btnSobre = self.findChild(QtWidgets.QPushButton,'btnSobre')
        self.btnSobre.clicked.connect(self.btnSobre_click)

        self.lblInfo = self.findChild(QtWidgets.QLabel, 'lblInfo')
        self.lblResult = self.findChild(QtWidgets.QLabel, 'lblResult')

        self.lstNegatives = self.findChild(QtWidgets.QListWidget, 'lstNegatives')
        self.txtFreqList = self.findChild(QtWidgets.QTextEdit, 'txtFreqList')

        self.txtInput = self.findChild(QtWidgets.QTextEdit, 'txtInput')
        self.show()
    
    def btnSobre_click(self):        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Orca Utilities")
        msg.setInformativeText("Author: Christiano dos Santos\ninfo:christiano.sts@gmail.com")        
        msg.setText("Version 2.0 - 12/10/2020")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
      
    ####     ctrl+C
    def clipboardChanged(self):
        text = str( QApplication.clipboard().text())
        clipboard = QApplication.clipboard()
        #clipboard.setText('test copia pra área de transferência')
        
        self.copia = text

    def copyItems(self):
        items = self.lstNegatives.selectedItems()
        x = []
        clipboard = QApplication.clipboard()
        
        for i in range(len(items)):
            x.append(str(self.lstNegatives.selectedItems()[i].text()))
        clipboard.setText(str(x))
            
    ####    limpa buffer
    def clear(self):        
        self.irData.clear()
        self.lstNegatives.clear()
        self.txtFreqList.clear()
        self.vibfreqList.clear()
        self.negativeFreq_list.clear()
        #self.txtInput.clear()

    def getDataObject(self, batchJob = False):        
        self.controller = Controller(self.dataObj)                
        self.dataObj =self.controller.getDataObject(self.dataObj.filename)
        
        inputText = self.dataObj.inputSection
        self.lblInfo.setText(self.labelHeader)
        if (not batchJob ):
            self.txtInput.append( inputText )
        self.txtInput.verticalScrollBar().setValue(self.txtInput.verticalScrollBar().minimum())
    
    #obtém os dados do arquivo na memoria: self.dataObj.filename
    def parseFile(self, batchJob = False):
        self.clear()        
        try:                
            # processa o arquivo e cria o objeto com os dados            
            self.getDataObject(batchJob)
            
            # obtém dados IR   
            self.getIR()           
            
        except Exception as e:
            self.lblResult.setText("ERRO NA LEITURA !!! \n " + str(e))
            
    # Obtém as frequências e adiciona na UI txtFreqList
    # def getFrequencies(self):        
    #     self.vibfreqList = self.controller.getFrequencies()
 
    #     for freq_value in self.vibfreqList:
            
    #         if '-' in freq_value:
    #             #QtGui.QColor
    #             self.lstNegatives.addItem(freq_value)
    #             self.txtFreqList.setTextColor(QColor(255, 0, 0))                
    #         else:
    #             self.txtFreqList.setTextColor(QColor(0, 0, 0))
    #         self.txtFreqList.append(freq_value)

    #     self.lblInfo.setText(self.labelHeader) 

    # obtém os dados do arquivo out, ASSINALA valores negativos SE HOUVER
    def getIR(self):
        
        self.vibfreqList =  self.dataObj.wavenum_list
        
        for spectrum_value in self.dataObj.irData_list:
            self.txtFreqList.append(spectrum_value)

        self.txtFreqList.verticalScrollBar().setValue(self.txtFreqList.verticalScrollBar().minimum())
        
        if len(self.dataObj.negative_waves_list)   > 0:
            for valor in  self.dataObj.negative_waves_list:
                self.lstNegatives.addItem(valor[0:5])   
            
            self.lblResult.setText(self.msgFrequenciaNegativa)
            self.lblResult.setStyleSheet("background-color: rgb(255, 0, 0);\n""color: rgb(255, 255, 0);")
                    
        else:
            self.lblResult.setText("Lucky guy!!! " +self.dataLegend)
            self.lblResult.setStyleSheet("background-color: rgb(0, 255, 0);\n""color: rgb(255, 0, 0);")
        
        if (len(self.vibfreqList) < 1):
            self.lblResult.setText(' nao encontrou freqs')
            self.lblResult.setStyleSheet("background-color: rgb(255, 0, 255);\n""color: rgb(255, 255, 255);")
    
    # Gera o gráfico com matplotlib
    def plot_graph(self, nome, x, y):
        wavenum = x             
        graph.figure(figsize=(8, 3))   #figsize define o tamanho na tela do graf gerado
        graph.plot(wavenum, y)
        graph.title(nome)    
        graph.axis([400,4000,0, 1.01])
        graph.plot(1)    
        graph.show()

    '''def gravar(self, arquivo, wave, calc_Intensity, normalizado, convertido):
        with open(arquivo, 'w') as outfile:
            for i in range(len(wave)):
                texto = str(wave[i]).replace(".",",") + ";" + str(calc_Intensity[i]).replace(".",",") \
                + ";" + str(normalizado[i]).replace(".",",") \
                + ";" + str(convertido[i]).replace(".",",") \
                + "\n"
                outfile.write(texto)
    '''
    #calcula a convolucao do espectro e grava
    def plotIR(self, irData, batchJob = False):
        # Extrair frequências e intensidades
        frequency = []
        T2_list = []
        for data in irData:
            freq, intensity = map(lambda x: float(x.replace(',', '.')), data.strip().split())
            frequency.append(freq)
            T2_list.append(intensity)

        # Configurações para a convolução
        wavemin = 400
        wavemax = 4001
        delta = 1
        omega = 10.0

         # Inicialização das listas de ondas e intensidades calculadas
        wave = list(range(wavemin, wavemax, delta))
        calc_Intensity = [0.0] * len(wave)

        # Fator de escala
        scale = 1.0
        
        ##################################################
         # p/ cd vibração da molécula tem um num de onda (frequency) e a intensidade T2
         # nessa conversão, 1o  usarei a escala de 400 (wavemin) a 4004, então seão 901 pontos
         # cd ponto é a somatória da contribuição de T2 em cada num de onda, com a expressão de Lorentz
         # omega = FWHH
        # Cálculo da convolução usando a expressão de Lorentz
        for j in range(len(wave)):
            for i in range(len(irData)):
                calc_Intensity[j] += scale * T2_list[i] * omega / (4 * (wave[j] - frequency[i])**2 + omega**2)

        # Normalização e conversão para absorbância
        max_intensity = max(calc_Intensity)
        normalized_intensity = [intensity / max_intensity for intensity in calc_Intensity]
        absorbance = [10 ** (-1 * intensity) for intensity in normalized_intensity]        
                
        # Caminho de saída para o arquivo CSV
        path, new_filename = os.path.split(self.dataObj.filename)
        output_file = os.path.join(path, f"{new_filename.rstrip('.out')}_Lorenz_IR_1cm_{omega}.csv")

        # Gravar os resultados no arquivo CSV
        try:
            self.controller.gravar(output_file, wave, calc_Intensity, normalized_intensity, absorbance)
            if not batchJob:
                self.plot_graph(self.dataObj.filename, wave, absorbance)
            if batchJob:
                self.txtInput.append("\n ARQUIVO CSV GERADO: " + output_file)
        except Exception as e:
            error_msg = f"**** Erro no arquivo **** : {output_file}\n{str(e)}"
            self.lblResult.setText(error_msg)
            print(error_msg)

    def checkFile(self, daoObj, batchJob = False):
        
        if daoObj.filename.isspace():
            self.lblResult.setText("arquivo vazio.")            
        else:            
            self.lblResult.setText(daoObj.filename)
            self.parseFile(batchJob)
    
    def btnBatchJob_click(self):
        rootDir = ''
        rootDir =  QFileDialog.getExistingDirectory(self,"Caminho Arquivos OUT",rootDir).replace('/','\\')
        self.gerarLoteEspectro(rootDir)

#gerar espectro de todos arquivos numa pasta
    def gerarLoteEspectro(self, pasta):
        self.txtInput.clear()
        self.txtInput.append( "GERANDO ESPECTROS EM LOTE \n" )
        for root, dirs, files in os.walk(pasta):
            for name in files:
                if '.out' in name:     
                    self.dataObj = DAO()               
                    self.dataObj.filename = root + "\\" + name

                    self.txtInput.append( self.dataObj.filename + "\n" )
                    self.checkFile(self.dataObj, True)
                    self.plotIR(self.dataObj.irData_list, batchJob=True)

    def btnAbrir_click(self):
        self.btnFileFind.setStyleSheet('QPushButton {background-color:cyan; font:bold}')        
        #rootDir = "F:\\MeusDocs\\Doutorado\\RESULTADOS\\SÓ_espectros"
        rootDir = "E:\\OrcaFiles\\new\\"
        if len(self.pastaOutput) == 0:  
            self.pastaOutput = rootDir;
        
        fileName = QFileDialog.getOpenFileName(self, "Open Output", self.pastaOutput, "Orca Files (*.out)")        
        self.dataObj = DAO()
        self.dataObj.filename = fileName[0]
        if (self.dataObj.filename != ''):
            self.txtInput.clear()
            self.pastaOutput = os.path.dirname(fileName[0])
            self.checkFile(self.dataObj)
            

    def btnIR_click(self):
        self.getIR()
        self.plotIR(self.dataObj.irData_list)
    
    def btnInput_click(self):
        #self.btnFileFind.setStyleSheet('QPushButton {background-color:cyan; font:bold}')        
        filter = "Coordinate Files (*.inp ) ;; Text files (*.txt)"
        
        if len(self.pastaInput) == 0:            
            self.pastaInput = QFileDialog.getExistingDirectory(self,"Caminho input","F:\\").replace('/','\\')
        
        fileXYZ,_ = QFileDialog.getOpenFileName(self, "Open XYZ .inp", self.pastaInput, filter )
        #inputDir = os.path.dirname(file)
        #print(inputDir)
        ''' 1- caminho dos inputs
            2- abrir xyz
            3- gerar
        '''
        try:
            c = InputGenerator(fileXYZ, self.pastaInput)
            c.inputCreator()
            self.lblResult.setText("Arquivos criados.")
            self.txtInput += c.result
        except Exception as e:
            self.lblResult.setText("Erro:\n"  + str(e))
        
      
app = QtWidgets.QApplication(sys.argv)
window = Ui()
sys.exit(app.exec_())