"""
Created on Thu August 07 10:00h 2021

@author: Christiano
    script para tratar os espectros gerados pelo prisma:
    1- Organizar os arquivos mol_dft_Lorenz_IR_1cm_10.0.csv em árvore de diretórios:
    -ANF - B3LYP
         - B3PW91
         - M062X
         - PEB0
    -BZD - B3LYP
         - B3PW91
         - M062X
         - PEB0
    idêntico para CAN, CAT e FEN
    nesse script, definir :
        ROOTDIR = diretório raiz para iniciar a busca e tratamento dos dados
        ARQUIVO_CONSOLIDADO = arquivo contendo os dados de todos espectros consolidados
        FILE_HEADER = cabeçalho do arquivo - nomes das colunas e valores de comprimento de onda
        esse cabeçalho tem espaço de 1 cm-1. caso mude o espectro gerado deverá ser adaptado de acordo
"""

import sys
import os.path
import pandas as pd

ROOTDIR = "F:\\MeusDocs\\Doutorado\\RESULTADOS\\Resultados_1cm\\"
#p = "F:\MeusDocs\Doutorado\RESULTADOS\Resultados_1cm"
ROOTDIR_cmsc = "E:\\Documentos\\doutorado\\RESULTADOS\\Resultados_1cm\\"
ROOTDIR = ROOTDIR_cmsc
ARQUIVO_CONSOLIDADO = ROOTDIR + "CONSOLIDADO_1cm.csv"

FILE_HEADER = "funcional;dft_class;molecula;sigla;grupo;"

# Gera uma lista de números de 400 a 4000 com incremento de 1
numeros = list(range(400, 4001, 1))

# Converte a lista de números em uma string separada por ponto e vírgula
string_numeros = ";".join(map(str, numeros))

FILE_HEADER = FILE_HEADER + string_numeros +  "\n";

# logica para ler o arquivo, extrair a linha com os dados e criar output
def processaArquivo(arquivo, dft, dftnum, mol, sigla, grp):
    
    dados = pd.read_csv( arquivo, sep=';', header=None, usecols=[3] )
    #valor = dados.iloc[0,0]
    #print(valor)
    nlinhas = len(dados)
    colecao = []
    for i in range(nlinhas):
        colecao.append(dados.iloc[i,0])
    #add grupo e metodo na str_data
    separador = ";"
    #string com a linha de dados: anf;B3LYP;    
    str_data =  dft + separador + dftnum + separador + mol + separador + sigla + separador + grp + separador 
    
    #adiciona os dados    
    for i in range(nlinhas):
        str_data += str(colecao[i]) + separador

    #trata o fim da linha
    str_data.rstrip(';')    
    str_data += "\n"

    return str_data

def getGrupo(pasta):
    if 'ANF' in pasta:
        return 'anf'
    if 'BZD' in pasta:
        return 'bzd'
    if 'CAN' in pasta:
        return 'can'
    if 'CAT' in pasta:
        return 'cat'
    if 'FEN' in pasta:
        return 'fen'

def getMetodo(pasta):
    if 'B3LYP' in pasta:
        return 'B3LYP'
    if 'B3PW91' in pasta:
        return 'B3PW91'
    if 'M06' in pasta:
        return 'M062X'
    if 'PBE0' in pasta:
        return 'PBE0'
    else: 
        return ''

def getMetodoNum(dft):
    if 'B3LYP' in dft:
        return '1'
    if 'B3PW91' in dft:
        return '2'
    if 'M06' in dft:
        return '3'
    if 'PBE0' in dft:
        return '4'
    else: 
        return ''

def getSigla(grp, contador):
    sigla =''
    if 'anf' in grp:
        sigla = 'a'
    if 'bzd' in grp:
        sigla = 'b'
    if 'can' in grp:
        sigla = 'c' 
    if 'cat' in grp:
        sigla = 'k'
    if 'fen' in grp:
        sigla = 'f'
    return sigla  + str(contador)

def salvar(resultado):
    with open(ARQUIVO_CONSOLIDADO, 'w') as outfile:        
        outfile.writelines(FILE_HEADER)
        outfile.write(resultado)
    print("arquivo salvo: ", ARQUIVO_CONSOLIDADO)

# Loop pelas subpastas A, B, C, CAT e F
subpastas = ['ANF', 'BZD', 'CAN', 'CAT', 'FEN']



 #colocar os arquivos .csv dos espectros organizados nas pastas de grupos e DFT  

 # VERIFICAR O NOME - SUFIXO: "_Lorenz_IR_1cm_10.0.csv"  
def captarDadosEspectros( pasta ):
    print("Processando arquivos das pastas e subpastas a partir de:\n", pasta)    
    grupo = ''
    metodo = ''
    sufixo = "_Lorenz_IR_1cm_10.0.csv"
    linha = ""
    final_str = ""
    contador = 0
    
    # ta gerando 3x no caso dos 4 dft, revisar ...
    
    for diretorio, subpastas, arqs in os.walk(pasta):
        #CONTA QTOS arquivos tem na pasta : 
        # como tenho o .out e .csv, fiz divisao por 2 pra montar a sigla
        
        for subpastaGrupo in subpastas:
            contador = 0
           
            dir_grupo = os.path.join(diretorio, subpastaGrupo)
            
           
            for classedir, molecdir, arquivos in os.walk(dir_grupo):
                dir_molec = os.path.join(diretorio, dir_grupo)
                
                grupo = getGrupo(dir_molec) # obtem o grupo
                metodo = getMetodo(classedir) #obtem o DFT
                
                pastaGrupo = os.path.join(ROOTDIR, subpastaGrupo)
                
                
                for arquivo in arquivos:  
                    arqfn = os.path.abspath(arquivo)
                    if arquivo.endswith('.csv'):           
                        contador += 1      
                        strRemove1 ="_Lorenz_IR_1cm_10.0.csv"
                        strRemove2 = "-PBE0-WATER_Lorenz_IR_1cm_10.0.csv" # p/ o arquivo com solvente
                        metodonum = getMetodoNum(metodo)
                        molecula = arquivo.replace(strRemove1,'') #obtém o nome da molecula
                        sigla = getSigla(grupo, contador)
                        
                        #  obter o fullname aqui
                        fullname = classedir + "\\" + os.path.relpath(arquivo) 
                        # #processaArquivo(arquivo, dft, mol, sigla, grp)  
                             
                        linha = processaArquivo(fullname, metodo, metodonum, molecula, sigla, grupo)

                        #print(grupo, metodo, molecula)                
                        final_str += linha
             

    return final_str      

resultado = captarDadosEspectros( ROOTDIR )
print("salvando em arquivo")
#salvar(resultado)