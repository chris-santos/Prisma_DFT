"""
Created on Mon October 10 10:00h 2020

@author: Christiano
    GUI para processar o arquivo de output do orca, gerar espectro, exportar dados
"""
from controller import Controller, DAO, InputGenerator
from dataLayer import DAO
from PyQt5 import QtWidgets, uic, QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
import sys
import os.path

# criar grafico IR
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
        #extrair freqs, Intensidade
        frequency = []  #  numero de onda de 1 vibração
        T2_list = [] # intensidade - valor do calculo dft
        lista = []
        nvib = (len(irData))
        for i in range(nvib):
            lista =irData[i].strip(" ").split() 
            frequency.append(float(lista[0].replace(',','.')))
            T2_list.append(float(lista[1].replace(',','.')))

        calc_Intensity = []
        wave = []
        wavemin =400
        wavemax = 4001 #(vai gerar de 400 a 4000)
        delta = 1
        npontos = int((wavemax - wavemin)/delta)
        omega = 10.0 # variar esse valor para mudar largura picos

        for i in range(wavemin, wavemax, delta):            
            calc_Intensity.append(0.0)
            wave.append(0.0)

        scale = 1.0   #scaling factor
        
        ##################################################
         # p/ cd vibração da molécula tem um num de onda (frequency) e a intensidade T2
         # nessa conversão, 1o  usarei a escala de 400 (wavemin) a 4004, então seão 901 pontos
         #cd ponto é a somatória da contribuição de T2 em cada num de onda, com a expressão de Lorentz
         # omega = FWHH
        path, arquivo = os.path.split(self.dataObj.filename)
        saida =  path + "//" + arquivo.rstrip(".out") + "_Lorenz_IR_1cm_" + str(omega) + ".csv" 
        try:
            if (omega > 0):
                for j in range(npontos):                
                    for i in range(0, nvib):  
                        wave[j] = (j * delta) + wavemin
                        calc_Intensity[j] += scale * T2_list[i] * omega/(4* (wave[j] - frequency[i])**2 + omega**2)
                        
            maximo = max(calc_Intensity)
            normalized = [valor/maximo for valor in calc_Intensity]
            convertido = [10**(-1 * valor) for valor in normalized]
        
       # saida = self.dataObj.filename.rstrip("out") + str(omega) + ".ir.csv"   
        #gravar( arquivo de saida, numero de onda, I calculado, I normalizado,  conversao pra absorbancia)        
        #self.gravar(saida, wave, calc_Intensity, normalized, convertido)
        #no excel, escolher a coluna 1 e 4 = grafico plotado 
       
            self.controller.gravar(saida, wave, calc_Intensity, normalized, convertido)
            
            if (not batchJob):
                self.plot_graph(self.dataObj.filename , wave, convertido)
            
            if (batchJob):
                self.txtInput.append( "\n ARQUIVO CSV GERADO: " + saida )

        except Exception as e:
            erroProc = "**** Erro no arquivo **** :" + saida + "\n" + str(e)
            self.lblResult.setText(erroProc)            
            print(erroProc)

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
        #rootDir = "F:\MeusDocs\Doutorado\RESULTADOS\SÓ_espectros"
        rootDir = "E:\OrcaFiles\\new\\"
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