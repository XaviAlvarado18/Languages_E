from tools.yapar_reader import YaParReader
from tools.reader import reader
import pickle

if __name__ == '__main__':
    content = reader('.\yapar\slr-3.yalp')
    Yapar = YaParReader(content)
    Yapar.obtain_productions()
    Yapar.generating_lr()
    print(Yapar)