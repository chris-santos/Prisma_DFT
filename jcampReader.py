"""
Created on Tue January 18 10:00h 2023

@author: Christiano dos Santos
    Rotina para leitura e extração dos dados de IR de arquivos JCAMP
    1- leitura do arquivo em pasta e nomes defininidos
    2- identificação dos caracteres indicadores dos dados de IR 
    3- impressão na saída padrão de informações das linhas com nome da molécula e o fatorY
    4- convolução e normalização dos dados usando gaussiana - parâmetros de resolução, ômega, etc podem ser variados
    e estão comentadas outras implementações - Lorentz
    5- criação de arquivo .csv do espectro IR normalizado (pasta/nome original + omega )
"""
#ler dados do jcamp-dx e gerar espectro
import math
import numpy as np
from scipy.special import wofz
import pylab


#arquivo ENFSI
pasta_raiz = "E:\\Documentos\\doutorado\\ARtigos\\2022\\Chris-benzos_IR\\benzo"
benzo_enf= "_ENFSI\\"
benzo_swg = "_swgdrug\\"
diretorio = pasta_raiz + benzo_swg
arquivoName = "b17" + "_swg"
arquivoExt = ".jdx"
print("***************************************************************")
print(arquivoName)

arquivoJcamp = diretorio + arquivoName + arquivoExt

linhas_conteudo = []
conteudo = []
STR_INICIO = "##XYDATA=(X++(Y..Y))"
#versao ensi TEM UM " " "##XYDATA= (X++(Y..Y))", to tratando isso na leitura
STR_INICIO = "##XYDATA=(X++(Y..Y))"
STR_END = "##END="
STR_FatorY = "##YFACTOR="


# abre o arquivo JCAMP e coloca o conteúdo na lista linhas_conteudo
try:
    with open(arquivoJcamp, 'rt') as outfile:
        #texto = outfile.read()
        for line in outfile:
            if not line.isspace():                
                    linhas_conteudo.append(line.rstrip("\n"))
except Exception as e:                
    print("*****    ERRO AO LER ARQUIVO:      *****\n " + str(e))
    print("\n*****    FIM ERRO AO LER ARQUIVO:      *****")
    
#  encontra a região com dados de Absorbância e fatorY
# em linhas_conteudo de acordo com as marcações 
for i in range(len(linhas_conteudo)):
    if i == 0:
        print(linhas_conteudo[i])
    if STR_INICIO in linhas_conteudo[i].replace(" ",""):
        input_start = i + 1
    if STR_END in linhas_conteudo[i]:
        input_end = i
    if STR_FatorY in linhas_conteudo[i]:
        fatorY = linhas_conteudo[i].lstrip(STR_FatorY)
        
fatorY = float(fatorY)  #
print("fator Y: " + str(fatorY))
print("")

# separa os dados do espectro em str
###XYDATA=(X++(Y..Y))
# 550,0 1153 774 545 609 412 304 531 730 752 863
# 590,0 942 1048 1192 1111 1014 831 688 735 771 851
# 630,0 926 849 856 873 847 991 1275 1471 1473 1655
frequency = []
dados= [valor.split() for valor  in linhas_conteudo[input_start:input_end]]
for i in range(len(dados)):
    frequency.append(float(dados[i][0]))
    
dados_jcamp = []
# lista auxiliar: converter para float em nova lista
for i in range(len(dados)):
    #print(dados[i])
    dados_jcamp.append(list(map(float, dados[i])))

#checando os tamanhos
#print("diferença: " + str(len(dados_jcamp) - len(linhas_conteudo[input_start:input_end])))

# cada linha tem vários valores de A
# calcular a média da absorbância, e salvar na lista: dados_media
dados_media = [ np.mean(valor[1:]) for valor in dados_jcamp]

# dados_jcamp[0] contém os numeros de onda
# print(dados_media[0])  # absorbancia média
'''
# impressao
for i in range(len(dados_media)):
    wn = str(frequency[i]).replace(".", ",")
    dm = str(fatorY*dados_media[i]).replace(".", ",")
    print(wn + " " +  dm)

'''
#print("")
# calcular %T  : T = 10^(-1 * A), sendo que A = fatorY * valor médio
dados_T = []
dados_T = [ 10**(-1 *(fatorY * valor)) for valor in dados_media]
#print(dados_T)
#normalização
#maximo = max(dados_T)
#print(maximo)

# convolução de Lorenz
calc_Intensity = []
wave = []
wavemin =400
wavemax = 4001 #(vai gerar de 400 a 4000)
delta = 1
npontos = int((wavemax - wavemin)/delta)
omega = 20.0 # variar esse valor para mudar largura picos


# zerando listas p armazenar valores de A e numero de onda
for i in range(wavemin, wavemax, delta):            
    calc_Intensity.append(0.0)
    wave.append(0.0)
try:
    if (omega > 0):
        for j in range(npontos):
            for i in range(0, len(dados_T)):
                wave[j] = wavemin + (j * delta) # 400, 401, 402...,
                # convolução I = Soma (A * omega / ((2 * no - f)^2 + omega^2)
                calc_Intensity[j] += fatorY * dados_media[i] * omega /  (4 * (wave[j] - frequency[i])**2 + omega**2)

    maximo = max(calc_Intensity)    
    normalized = [valor/maximo for valor in calc_Intensity]
    #calcula T
    convertido =  [10**(-1 * valor) for valor in normalized]       
except Exception as e:                
    print(str(e))

result = ""
"""
    Encontrar um novo valor de nu("freq") através de uma expressão de Lorentz
    cada novo valor Ilorentz = Somatório(I * w/ ( 4* (nu - n0)^2 +w^2) artigo: IR-Lorentz-Eps-29June2015
    n0 = valor numero de onda 
"""
# convolucao Lorentziana - 
# sigma = largura ; nvib = len(dados_T) qtd de pontos medidos
# list_intensity = dados_media: lista com valores de A
# list_wavenumber: lista com os números de onda = lista frequency
def lorentzCurve(omega, nvib, list_intensity, list_wavenumber):
    if (omega > 0):
        for j in range(npontos):            
            for i in range(0, nvib):
                wave[j] =  wavemin + (j * delta) # 400, 408, 416, 424, ...
                deltaNu = wave[j] - list_wavenumber[i]
                alfa = omega/(4* deltaNu**2 + omega**2)
                A = list_intensity[i]
                calc_Intensity[j] += fatorY * A * alfa
                #print(calc_Intensity[j])
    
    TRANSMITANCIA = [10**(-1 * valor) for valor in calc_Intensity]
    
    maximo = max(TRANSMITANCIA)
    minimo = min(TRANSMITANCIA)
    
    Tnormalized = [(valor - minimo)/(maximo - minimo) for valor in TRANSMITANCIA]
    #Tnormalized = [valor/maximo for valor in TRANSMITANCIA]
    
    return Tnormalized
    #print(convertido)

def getTransmitanceSpectra(omega, list_Int, list_wavenum):
    w = omega
    nvib = len(dados_T)
    if (w > 0):        
        for j in range(npontos):            
            for i in range(0, nvib):
                A = list_Int[i]             
                wave[j] =  wavemin + (j * delta) # 400, 408, 416, 424, ...  
                deltaNu = wave[j] - list_wavenum[i]
                cte = 27.614  # 200/(pi x ln(10))       
                alfa = cte * w/(((2*deltaNu)**2) + w**2 )
                
                calc_Intensity[j] += fatorY * A * alfa
                #print(calc_Intensity[j])    
    maximo = max(calc_Intensity)
    Tnormalized = [valor/maximo for valor in calc_Intensity]    
    
    return Tnormalized   
                
def otherLorentz(omega, list_Int, list_wavenumber):
    w = omega
    nvib = len(dados_T)
    if (w > 0):        
        for j in range(npontos):            
            for i in range(0, nvib):
                A = list_Int[i]             
                wave[j] =  wavemin + (j * delta) # 400, 408, 416, 424, ...  
                deltaNu = wave[j] - list_wavenumber[i]
                cte = 27.614  # 200/(pi x ln(10))       
                alfa = cte * w/(((2*deltaNu)**2) + w**2 )
                
                calc_Intensity[j] += fatorY * A * alfa
                #print(calc_Intensity[j])    
    
    TRANSMITANCIA = [10**(-1 * valor) for valor in calc_Intensity]
    maximo = max(TRANSMITANCIA)
    minimo = min(TRANSMITANCIA)
    
    Tnormalized = [(valor - minimo)/(maximo - minimo) for valor in TRANSMITANCIA]
    #print(normalized)
    
    
    return Tnormalized

# convolucao gaussiana - 
# sigma = largura ; nvib = len(wave) qtd de pontos medidos
# list_intensity = calc_Intensity: lista com valores de A
# list_wavenumber: lista com os números de onda = lista frequency
def gaussianCurve(sigma, nvib, list_intensity, list_wavenumber):
    if (omega > 0):
        for j in range(npontos):
            for i in range(0, int(nvib)):               
                wave[j] = (j * delta) + wavemin
                alfa = -1 * (( (wave[j] - list_wavenumber[i])/ (sigma/2) )**2 )
                calc_Intensity[j] += fatorY * list_intensity[i] * math.exp( alfa )
                #print(calc_Intensity[j])
    maximo = max(calc_Intensity)
    normalized = [valor/maximo for valor in calc_Intensity]
    #print(normalized)
    converted = [10**(-1 * valor) for valor in normalized]
    #print(converted)
    return converted     
         
   
# grava um arquivo baseado nos valores contidos nas listas:
# convertido = resultado da convolução
# wave = os números de onda: linha 86
# converte p/ string trocando o decimal, p/ o excel
def gravar( arquivo ):
    result = ""
    with open(arquivo, 'w') as outfile:
        for i in range(len(convertido)) :
            freq = str(wave[i])
            t = convertido[i]
            result += freq.replace(".", ",")+ ";" + str(t).replace(".", ",") + "\n"
        outfile.write(result)
    print(" arquivo gerado: " +  arquivoName + " \n " + arquivo)
    print("*************************************************************** \n")

'''
arquivoSaida = arquivoJcamp + "_exp_" + str(omega) + "_MaxMin.csv"
convertido = lorentzCurve(omega, len(dados_T), dados_media, frequency )

# vou comentar aqui pra salvar a media
# gravar(arquivoSaida)

'''
arquivoSaida = arquivoJcamp + "_exp_Gaussian_" + str(omega) + ".csv"
convertido = gaussianCurve(omega, len(dados_T), dados_media, frequency )
#print(convertido)
gravar(arquivoSaida)

#arquivoSaida = arquivoJcamp + "_exp_calc_T_Norm" + str(omega) + ".csv"
#convertido = getTransmitanceSpectra(omega, dados_media, frequency )
#gravar(arquivoSaida)



#arquivoSaida = arquivoJcamp + "_exp_calc_T_Norm" + str(omega) + ".csv"
#convertido = otherLorentz(omega, dados_media, frequency )
#gravar(arquivoSaida)



