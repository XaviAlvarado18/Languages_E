import pickle
import subprocess
from yapar_main import SLR_simulate
from tools.reader import reader


oScan = './tokens/tokens2.txt'  
yapar = './yapar_scanner/scan_yapar2_ext.pkl'   

if oScan is None or yapar is None:
    raise Exception('Debes proporcionar los archivos de escaneo, escaneo de salida y objeto yapar')

#subprocess.run(readTokensCommand)
#reader.graphLRO()

with open(yapar, 'rb') as yaparFile:
    tableSLR = pickle.load(yaparFile)

print('Producciones:')
print(tableSLR.product_list_toPrint)

content = reader(oScan)
print(oScan, content)

SLR_simulate(content, tableSLR)