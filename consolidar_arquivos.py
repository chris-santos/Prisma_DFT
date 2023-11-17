

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

import os
import pandas as pd

root_folder = "E:\\Documentos\\doutorado\\RESULTADOS\\Resultados_1cm"
ROOTDIR = root_folder
ARQUIVO_CONSOLIDADO = ROOTDIR + "\\CONSOLIDADO_1cm_semvirgula.csv"

grupos = os.listdir(root_folder)

grupo_siglas = {}
funcional_siglas = {}

FILE_HEADER = "funcional;dft_class;molecula;sigla;grupo;"

# Gera uma lista de números de 400 a 4000 com incremento de 1
numeros = list(range(400, 4001, 1))

# Converte a lista de números em uma string separada por ponto e vírgula
string_numeros = ";".join(map(str, numeros))

FILE_HEADER = FILE_HEADER + string_numeros +  "\n";

def processaArquivo(arquivo, dft,  mol, sigla):
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
    str_data =  dft + separador + mol + separador +  sigla  
    
    #adiciona os dados    
    for i in range(nlinhas):
        str_data += str(colecao[i]) + separador

    #trata o fim da linha
    str_data.rstrip(';')    
    str_data += "\n"

    return str_data

def salvar(resultado):
    with open(ARQUIVO_CONSOLIDADO, 'w') as outfile:        
        outfile.writelines(FILE_HEADER)
        outfile.write(resultado)
    print("arquivo salvo: ", ARQUIVO_CONSOLIDADO)


def getSigla(grp, contador):
    sigla =''
    if 'ANF' in grp:
        sigla = 'a'
    if 'BZD' in grp:
        sigla = 'b'
    if 'CAN' in grp:
        sigla = 'c' 
    if 'CAT' in grp:
        sigla = 'k'
    if 'FEN' in grp:
        sigla = 'f'
    return sigla  + str(contador)

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
    
def captarDadosEspectros():
    final_str = ""
    for grupo in grupos:
        grupo_path = os.path.join(root_folder, grupo)
        if os.path.isdir(grupo_path):
            grupo_siglas[grupo] = {}
            
            funcionais = os.listdir(grupo_path)
            contador = 1
            for funcional in funcionais:
                funcional_path = os.path.join(grupo_path, funcional)
                if os.path.isdir(funcional_path):
                    funcional_siglas[funcional] = {}
                    
                    nsp_folders = os.listdir(funcional_path)
                    
                    for nsp_folder in nsp_folders:
                        
                        nsp_path = os.path.join(funcional_path, nsp_folder)
                        if os.path.isdir(nsp_path):
                            arquivos_csv = [arquivo for arquivo in os.listdir(nsp_path) if arquivo.endswith('.csv')]
                            grupo_sigla = f'{getSigla(grupo, contador)};{grupo};'
                            funcional_sigla = f'{funcional};{getMetodoNum(funcional)}'
    #
                            for arquivo in arquivos_csv:
                                # processar arquivo
                                sufixo = '_Lorenz_IR_1cm_10.0.csv'
                                strRemove = f'-{funcional}{sufixo}'
                                molecula = arquivo.replace(strRemove,'') 
                                
                                # processar
                                arquivo_nsp = os.path.join(nsp_path, arquivo)
                                linha = processaArquivo(arquivo_nsp, funcional_sigla, molecula, grupo_sigla)
                                final_str += linha
                                #grupo_siglas[grupo][arquivo] = grupo_sigla
                                #funcional_siglas[funcional][arquivo] = funcional_sigla
                        contador += 1
    return final_str   

print("salvando em arquivo")
resultado = captarDadosEspectros()
#salvar(resultado)
