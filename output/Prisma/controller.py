"""
Created on Mon October 10 10:00h 2020

@author: Christiano
processar o arquivo de output

#auto-py-to-exe -nc - seção aditional: projeto.ui
#https://nitratine.net/blog/post/issues-when-using-auto-py-to-exe/?utm_source=auto_py_to_exe&utm_medium=application_link&utm_campaign=auto_py_to_exe_help&utm_content=bottom#installation


"""
# parse file
# getInput() - lista str
# getFrequencies() - lista str - converte . em ,
# getNegativeFreqs() - lista str
# getInputSection() - lista str

from dataLayer import DAO
class Controller:    
    input_section = ''
    
    def __init__(self, dataobject):
        self.lines = []
        self.vibfreqList = []
        self.VIBRATIONAL_str = "VIBRATIONAL FREQUENCIES"
        self.NORMAL_MODES_str = "NORMAL MODES"
        self.NORMAL_MODES_str = "NORMAL MODES"
        self.IR_SPECTRUM_str = "IR SPECTRUM"
        self.dao = dataobject 

# obter as linhas do arquivo como um texto
    def getOutputData(self, arquivo  ):                
        try:
            with open(arquivo, 'rt') as outfile:
                #texto = outfile.read()
                for line in outfile:
                    if not line.isspace():
                        self.dao.output_lines.append(line.rstrip("\n"))
                        self.lines.append(line.rstrip("\n"))
        except Exception as e:                
                print(str(e))
        #return self.dao

    def getDataObject(self, arq):
        self.getOutputData(arq)
        input_str = 'INPUT FILE'
        input_end_str = 'END OF INPUT'
        input_start = 0
        input_end = 0
        input_lines = ''
        for i in range(len(self.dao.output_lines)):
            if input_str in self.dao.output_lines[i]:
                    #print('input starts in line:' , i)
                input_start = i
            if input_end_str in self.dao.output_lines[i]:
                input_end = i

        inpline = input_start + 2
        input_name = self.dao.output_lines[inpline]
        
        for i in range(inpline,input_end):
            input_lines += (self.dao.output_lines[i][6:]) + "\n"
        
        self.dao.inputSection = input_lines
        self.getFrequencies()
        self.getIR()
        return   self.dao      

    def getFrequencies(self):
        vibr_start = 0
        vibr_end = 0

        for i in range(len(self.dao.output_lines)):
            if self.dao.VIBRATIONAL_str in self.dao.output_lines[i]:
                #print('input starts in line:' , i)
                vibr_start = i
            if self.dao.NORMAL_MODES_str in self.dao.output_lines[i]:
                vibr_end = i - 1     
                break   

        #LISTA DE FREQUENCIAS
        for i in range(vibr_start + 4,vibr_end):
            freq_value = self.dao.output_lines[i][6:].rstrip('cm**-1').strip().replace('.',',')            
            self.dao.wavenum_list.append(freq_value)  
            if '-' in freq_value:
                self.dao.negative_waves_list.append(freq_value.lstrip())        
        #return self.dao.wavenum_list

    def getIR(self):
        IR_start = 0
        IR_end = 0  
        for i in range(len(self.dao.output_lines)):
            if self.IR_SPECTRUM_str in self.dao.output_lines[i]:                    
                IR_start = i
                break
        for i in range(IR_start, len(self.dao.output_lines) ):
            if ("The first frequency") in self.dao.output_lines[i]:
                IR_end = i
                break
        # criar LISTA DE dados
            '''
            Mode    freq (cm**-1)   T**2         TX         TY         TZ
            -------------------------------------------------------------------
                6:         9.99    0.246378  ( -0.092991  -0.400685   0.277816)
            '''
        for i in range(IR_start + 4,IR_end):
            spectrum_value = self.dao.output_lines[i][10:30].replace('.',',')                
            self.dao.irData_list.append(spectrum_value.lstrip())            
            #self.txtFreqList.append(spectrum_value)                
            
                #self.lstNegatives.addItem(self.dao.output_lines[i][10:18])
        #print(len(self.dao.irData_list))

    def gravar(self, arquivo, wave, calc_Intensity, normalizado, convertido):
        with open(arquivo, 'w') as outfile:
            for i in range(len(wave)):
                texto = str(wave[i]).replace(".",",") + ";" + str(calc_Intensity[i]).replace(".",",") \
                + ";" + str(normalizado[i]).replace(".",",") \
                + ";" + str(convertido[i]).replace(".",",") \
                + "\n"
                outfile.write(texto)
class InputGenerator:
    """
    controller class with input file creation methods. takes xyzfile and  inputfilePath as args
    """
    def __init__(self, xyzfile, inpPath):
        self.fileB3LYP = inpPath + "\\b3lyp.txt"
        self.fileB3PW91 = inpPath + "\\b3PW91.txt"
        self.fileM062X = inpPath + "\\M062X.txt"
        self.fileXYZ = xyzfile                
        self.B3LYP = ''
        self.B3PW91 = ''
        self.M062X = ''
        self.header = ''
        self.XYZ = ''
        self.inputDir = inpPath
        self.result = ""

        
    def writeInput(self, prefix, arquivo, metodo):    
        try:
            with open(arquivo, 'w') as outfile:
                inputStr =  prefix +  metodo + "\n" + self.XYZ
                outfile.write(inputStr)
                return outfile.name
        except Exception as e:
            return str(e)
        

    def inputCreator(self):  
        try:
            with open(self.fileB3LYP, 'rt') as outfile:
                self.B3LYP = outfile.read()

            with open(self.fileB3PW91, 'rt') as outfile:
                self.B3PW91 = outfile.read()

            with open(self.fileM062X, 'rt') as outfile:
                self.M062X = outfile.read()

            with open (self.fileXYZ, 'rt') as outfile:
                self.header = outfile.readline().rstrip("\n")
                self.XYZ = outfile.read()
        except Exception as e:            
            print(str(e))

        dftInput = [self.B3LYP, self.B3PW91 , self.M062X]
        dftName = ['B3LYP', 'B3PW91', 'M062X']

        molecula = self.header.lstrip("# ")

        for i in [0,1,2]:
            prefix =  self.header + "-" + dftName[i]   + "\n"
            arquivo = self.inputDir +"\\" + molecula + "-" + dftName[i] + ".inp"
            self.result += self.writeInput(prefix, arquivo, dftInput[i]) +"\n"
    

