from tools.yapar_reader import YaParReader
from tools.reader import reader
import pickle

if __name__ == '__main__':
    content = reader('.\yapar\slr-1.yalp')
    reader2 = YaParReader(content)
    print(content)