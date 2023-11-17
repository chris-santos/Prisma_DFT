#**********************************************************************************
#   author: Christiano dos Santos - 05/10/2020
# program to process  ORCA output data:
#  1- open output file
#  2- parse the IR output
#  3- two methods for convolutioning: Gaussian and Lorentz
#  4- generate graph
#  5- convert to .csv format 
#**********************************************************************************
import matplotlib.pyplot as graph
import math

#ler arquivo 
fileName = "F:\ORCA4\\24-DMCC\\2MEC\\2-MEC-B3LYP.out.ir.stk"
irData = []
with open(fileName, 'rt') as outfile:
    #texto = outfile.read()
    for line in outfile:
        if not line.isspace():
            irData.append(line.rstrip("\n"))
            
#extrair freqs, Intensidade
frequency = []
T2_list = []
test = irData[0].strip(" ").split()

nvib = (len(irData))

for i in range(nvib):
    lista =irData[i].strip(" ").split() 
    frequency.append(float(lista[0]))
    T2_list.append(float(lista[1]))

calc_Intensity = []
wave = []
wavemin =400
wavemax = 4000
delta = 2
npontos = int((wavemax - wavemin)/delta)

for i in range(wavemin, wavemax, delta):
    #print(i)
    calc_Intensity.append(0.0)
    wave.append(0.0)

scale = 1.0   #scaling factor
omega = 20.0 # variar esse valor

def gravar(arquivo, wave, calc_Intensity, normalizado, convertido):
    with open(arquivo, 'w') as outfile:
        for i in range(len(wave)):
            texto = str(wave[i]).replace(".",",") + ";" + str(calc_Intensity[i]).replace(".",",") \
            + ";" + str(normalizado[i]).replace(".",",") \
            + ";" + str(convertido[i]).replace(".",",") \
            + "\n"
            outfile.write(texto)

# método para gerar o gráfico
def plot_graph(nome, x, y):
    wavenum = x     
    graph.figure(figsize=(16, 8))
    graph.plot(wavenum, y)
    graph.title(nome)    
    graph.plot(1)
    
    graph.show()

"""
    Encontrar um novo valor de nu("freq") através de uma expressão de Lorentz
    cada novo valor Ilorentz = Somatório(I * w/ ( 4* (nu - n0)^2 +w^2)
"""
def lorentzCurve(omega, nvib, list_intensity, list_wavenumber):
    if (omega > 0):
        for j in range(npontos):
            
            for i in range(0, nvib):
                wave[j] = (j * delta) + wavemin
                calc_Intensity[j] += scale * list_intensity[i] * omega/(4* (wave[j] - list_wavenumber[i])**2 + omega**2)
                #print(calc_Intensity[j])
    maximo = max(calc_Intensity)
    normalized = [valor/maximo for valor in calc_Intensity]
    convertido = [10**(-1 * valor) for valor in normalized]
    #print(convertido)
    saida = "F:\ORCA4\\24-DMCC\\2MEC\\2MEC.lorenz_spectro_w" + str(omega) + ".ir.csv"           
    #gravar(saida, wave, calc_Intensity, normalized, convertido)
    plot_graph(" IR via DFT calculation (Lorentz shape convolution)", wave, convertido)

# Gaussian
#units:  scale: n/a
#       intesity: km/mol
#       wavenumber = 1/cm
#       sigma = 1/cm
"""
    Encontrar um novo valor de nu("freq") através de uma Gaussiana
    cada novo valor de Igauss= Somatório(I * e( -(( nu - n0)/sigma)^2 )
"""
def gaussianCurve(sigma, nvib, list_intensity, list_wavenumber):
    if (omega > 0):
        for j in range(npontos):
            for i in range(0, int(nvib)):               
                wave[j] = (j * delta) + wavemin

                alfa = -1 * (( (wave[j] - list_wavenumber[i])/ (sigma/2) )**2 )
                calc_Intensity[j] += scale * list_intensity[i] * math.exp( alfa )
                #print(calc_Intensity[j])
    maximo = max(calc_Intensity)
    normalized = [valor/maximo for valor in calc_Intensity]
    #print(normalized)
    converted = [10**(-1 * valor) for valor in normalized]
    #print(converted)
    saida = "F:\ORCA4\\24-DMCC\\2MEC\\2MEC.spectro_gaussian_w" + str(sigma) +".ir.csv"           
    #gravar(saida, wave, calc_Intensity, normalized, converted)
    plot_graph(" IR via DFT calculation (Gaussian shape convolution)", wave, converted)

def gaussianPedroCurve(sigma, nvib, list_intensity, list_wavenumber):
    if (omega > 0):
        for j in range(npontos):
            for i in range(0, int(nvib)):               
                wave[j] = (j * delta) + wavemin

                alfa =  (( (wave[j] - list_wavenumber[i]) **2)/ sigma) 
                calc_Intensity[j] += scale * list_intensity[i] * math.exp(-1 * alfa )
                #print(calc_Intensity[j])
    maximo = max(calc_Intensity)
    normalized = [valor/maximo for valor in calc_Intensity]
    #print(normalized)
    converted = [10**(-1 * valor) for valor in normalized]
    print(calc_Intensity[0:5])
    saida = "F:\ORCA4\\24-DMCC\\2MEC\\2MEC.spectro_Pedro_w" + str(sigma) +".ir.txt"           
    #gravar(saida, wave, calc_Intensity, normalized, converted)

#lorentzCurve(10,nvib,T2_list,frequency)
gaussianCurve(20, nvib, T2_list, frequency)
#gaussianPedroCurve(100, nvib, T2_list, frequency)

if (omega == 0):
    wave[1] = 0
    j = 3
    for i in range(1, nvib +1):
        wave[j-1] = frequency[i] - 0.01
        wave[j]   = frequency[i]
        calc_Intensity[j]=scale*T2_list[i]
        wave[j+1] = frequency[i] + 0.01
        j=j+3
    wave[j-1] = 4000.0
    wavemax = j-1



