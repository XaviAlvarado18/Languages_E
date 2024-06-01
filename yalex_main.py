from tools.yalex_reader import *
from tools.reader import *

if __name__ == '__main__':
    source = './yalex/conflicto.yal'
    output = './yalex_scanner/conflicto.py'
    
    content = reader(source)
    ev = evaluate_text(content)
    for tk, m in ev:
        if tk == 1:
            raise Exception('Error in', m)

    if getTotal() == 0:
        raise Exception('No tokens found')

    codes = create_mach(False, output)

    for files in codes:
        print('Archivo creado: ', files)
