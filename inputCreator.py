# CRIAR INPUTS ORCA


SPACE = "*********************************************************************************"
#ler arquivo 
caminho = "F:\ORCA4\inputs\Anfetamina\\"
fileB3LYP = "F:\ORCA4\\inputs\\b3lyp.txt"
fileB3PW91 = "F:\ORCA4\\inputs\\b3PW91.txt"
fileM062X = "F:\ORCA4\\inputs\\M062X.txt"
fileXYZ = caminho + "amphetamine.xyz"

with open(fileB3LYP, 'rt') as outfile:
    B3LYP = outfile.read()

with open(fileB3PW91, 'rt') as outfile:
    B3PW91 = outfile.read()

with open(fileM062X, 'rt') as outfile:
    M062X = outfile.read()

with open (fileXYZ, 'rt') as outfile:
    header = outfile.readline().rstrip("\n")
    XYZ = outfile.read()

dftInput = [B3LYP, B3PW91 , M062X]
dftName = ['B3LYP', 'B3PW91', 'M062X']
#auto-py-to-exe -nc - seção aditional: projeto.ui
#https://nitratine.net/blog/post/issues-when-using-auto-py-to-exe/?utm_source=auto_py_to_exe&utm_medium=application_link&utm_campaign=auto_py_to_exe_help&utm_content=bottom#installation


def gravar(prefix,arquivo, metodo):    
    with open(arquivo, 'w') as outfile:
        inputStr =  prefix +  metodo + "\n" + XYZ

        outfile.write(inputStr)

#print('header: ',  header)
molecula = header.lstrip("# ")
#print(molecula)

def testgravar(prefix, arquivo, metodo):
    inputStr =  prefix +  metodo + "\n" + XYZ
    
    print(inputStr)
    

for i in [0,1,2]:
    prefix =  header + "-" + dftName[i]   + "\n"
    arquivo = caminho + molecula + "-" + dftName[i] + ".inp"  
    gravar(prefix, arquivo, dftInput[i]) 
    #gravar(sufix, arquivo, dftInput[i]) 
