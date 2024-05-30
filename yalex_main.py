from tools.yalex_reader import *
from tools.reader import *

if __name__ == '__main__':
    source = './yalex/slr-2_ext.yal'
    output = './yalex_scanner/scan_yalex2_ext.py'
    
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
