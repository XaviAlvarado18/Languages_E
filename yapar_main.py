from tools.reader import reader
import pickle
import pandas as pd
import tabulate
from tools.Classes_ import Grammar_Element, Production_Item, LRO_S, SLR_Table
from tools.Simulator import exclusiveSim
from tools.AFD import *
from tools.draw import draw_LR0

class YaParReader:
    def __init__(self, content):
        self.action_table2 = None
        self.table_printG: pd.DataFrame = pd.DataFrame()
        self.organize_list = None
        self.content = content
        self.error = False
        self.tokens: Dict[str, Grammar_Element] = dict()
        self.productions: Dict[str, Grammar_Element] = dict()
        self.FirstState = None
        self.predictive_table = None
        self.goto_table: pd.DataFrame = pd.DataFrame()
        self.table_printG2: pd.DataFrame = pd.DataFrame()
        self.action_table: pd.DataFrame = pd.DataFrame()
        self.firstProduct: 'Production_Item' or None = None
        self.symbols: Set[Grammar_Element] = set()
        self.lr0_states: Dict[int, LRO_S] = dict()
        self.LR0: LRO_S or None = None
        self.prsDict: Dict[int, Production_Item] = {}
        self.prod_list_toPrint = ''

    def obtain_productions(self):
        organize_machine = import_module('yaPar_reader.py',
                                         {
                                             'TK_SECTION': ['%token ([A-Z]| )+', 'IGNORE ([A-Z]| )+'],
                                             'PRODUCTION': ['[a-z]+:([a-zA-Z]| |\n|\|)+;'],
                                             'COMMENT': ['//.*\n', '/\*([^*/]|[^/]\*[^/]|[^*]/[^*])*\*/']
                                         })

        self.organize_list = exclusiveSim(organize_machine, self.content)
        prs = {}
        for message, tk in self.organize_list:
            if tk == 1:
                self.error = True
                break
            if tk == 'TK_SECTION':
                if '%token' in message:
                    message = message.replace('%token', '').strip()
                    message = message.split(' ')
                    for m in message:
                        self.tokens[m] = Grammar_Element(m, terminal=True)
                        self.symbols = self.symbols.union({self.tokens[m]})
                elif 'IGNORE' in message:
                    message2 = message.replace('IGNORE', '').strip()
                    message2 = message2.split(' ')
                    for m in message2:
                        if m in self.tokens:
                            self.tokens[m].ignore = True
                        else:
                            raise Exception('Token not found in', message)
                continue
            if tk == 'PRODUCTION':
                message2 = message.split(':')
                prName = message2[0]
                if prName in self.productions:
                    raise Exception('Production already exists', message)
                self.productions[message2[0]] = Grammar_Element(message2[0])
                self.symbols = self.symbols.union({self.productions[message2[0]]})
                if self.FirstState is None:
                    self.FirstState = self.productions[message2[0]]
                message2 = message2[1][:-1].strip().split('|')
                prs[prName] = message2

        count_prod = 2
        for key in self.productions:
            for pr in prs[key]:
                pr = pr.strip().split(' ')
                production = []
                for p in pr:
                    if p in self.tokens:
                        production.append(self.tokens[p])
                    elif p in self.productions:
                        production.append(self.productions[p])
                    else:
                        raise Exception('Token not found in definition to production', key, p)

                self.prsDict[count_prod] = self.productions[key].transition_to(production, count_prod)
                count_prod += 1

        newInit = Grammar_Element(self.FirstState.value + "\'")
        lastState = Grammar_Element('$', terminal=True)
        self.tokens['$'] = lastState
        self.firstProduct = newInit.transition_to([self.FirstState, lastState], 1)
        self.prsDict[1] = self.firstProduct
        self.FirstState = newInit
        self.productions[newInit.value] = newInit

        self.FirstState.calculateFirst()
        self.FirstState.calculateFollow()
        self.FirstState.resetFirstFollow()
        for val in self.productions.values():
            val.resetFirstFollow()
            val.calculateFirst()
            val.calculateFollow()

        for pr in self.productions.values():
            print(pr.value, '-> First: ', {x.value for x in pr.first}, 'Follow:', {x.value for x in pr.follow})

        return self.content

    def generating_lr(self):
        count = 1
        initState = LRO_S(self.firstProduct.closureCalc(), 0)
        self.lr0_states[0] = initState
        toEvaluate = [initState]
        lrsStates = {initState: initState}

        while toEvaluate:
            state = toEvaluate.pop(0)
            for symbol in self.symbols:
                newState = set()
                for item in state.state:
                    passItem, newItem = item.passPoint(symbol)
                    if passItem:
                        closureNewItem = newItem.closureCalc()
                        for i in closureNewItem:
                            newState.add(i)

                if newState:
                    newLR0 = LRO_S(newState, count)
                    if newLR0 not in lrsStates:
                        lrsStates[newLR0] = newLR0
                        toEvaluate.append(newLR0)
                        self.lr0_states[count] = newLR0
                        count += 1
                    else:
                        newLR0 = lrsStates[newLR0]
                    state.transitions[symbol] = newLR0

        self.LR0 = initState
        #print("initState: ", initState)
        return initState

    def graph_lr0(self):
        if self.LR0 is None:
            self.LR0 = self.generating_lr()

        draw_LR0(self.LR0, 'AF', 'default')
        #draw_LR0(self.LR0, 'AF', 'default', useNum=True)

    def obtain_grammar_element(self, value):
        return self.tokens.get(value)

    def get_item(self, value):
        return self.prsDict.get(value)

    def get_slr_table(self):
        self.action_table = pd.DataFrame(columns=[str(x.value).strip() for x in self.symbols] + ['$'],
                                          index=[str(x) for x in range(len(self.lr0_states))])
        self.action_table2 = self.action_table.copy()
        self.table_printG = self.action_table.copy()

        print('States LR0')

        for num, state in self.lr0_states.items():
            for item in state.non_completed_Ter:
                term = item.poitElement()
                if term.value == '$':
                    self.action_table.at[str(num), '$'] = ('A', [])
                    self.action_table2.at[str(num), '$'] = ('A', [])
                    self.table_printG.at[str(num), '$'] = "Accept!"
                    continue
                self.action_table.at[str(num), str(term.value)] = ('S', state.transitions[term])
                self.action_table2.at[str(num), str(term.value)] = ('S', state.transitions[term].numState)
                self.table_printG.at[str(num), str(term.value)] = 'S' + str(state.transitions[term].numState)

            for item in state.non_completed_NonTer:
                nonTerm = item.poitElement()
                self.action_table.at[str(num), str(nonTerm.value).strip()] = ('Goto', state.transitions[nonTerm])
                self.action_table2.at[str(num), str(nonTerm.value).strip()] = ('Goto', state.transitions[nonTerm].numState)
                self.table_printG.at[str(num), str(nonTerm.value).strip()] = state.transitions[nonTerm].numState

            for item in state.complete:
                if item.original == self.firstProduct:
                    continue

                first = item.NonTerminal.follow
                for f in first:
                    self.action_table.at[str(num), str(f)] = ('R', self.prsDict[item.count])
                    self.action_table2.at[str(num), str(f)] = ('R', (self.prsDict[item.count].NonTerminal.value,
                                                                     len(self.prsDict[item.count].Result)))
                    self.table_printG.at[str(num), str(f)] = 'R' + str(item.count)

        print('table')
        print(tabulate.tabulate(self.table_printG, headers='keys', tablefmt='psql'))
        toIgnore = {elem.value for elem in self.tokens.values() if elem.ignore}
        for key in sorted(self.prsDict.keys()):
            item = self.prsDict[key]
            print(key, str(item), str(item.count))
            self.prod_list_toPrint += str(key) + ' ' + str(item) + '\n'
        return SLR_Table(self.action_table2, self.table_printG, set(self.tokens.keys()), self.LR0.numState, toIgnore,
                         product_list_toPrint=self.prod_list_toPrint)

    def obtain_action(self, state, symbol):
        return self.action_table.at[str(state), str(symbol)], self.table_printG.at[str(state), str(symbol)]
    
    

def SLR_simulate(content:str, reader: 'SLR_Table'):
    contentTokens: List[str] = []
    for element in content.split(' '):
        el = element.strip()
        if el == '':
            continue
        tk = reader.obtainGrammarElement(el)
        if tk == 1:
            raise Exception('Token not found in', element)
        if tk == 2:
            continue
        contentTokens.append(el)

    contentTokens.append('$')

    stateStack: List[int] = [reader.firstState]
    df_stack = {}

    while True:
        stateOn = stateStack[-1]
        actualToken = contentTokens[0]
        action, desc = reader.obtainAction(stateOn, actualToken)
        df_stack['State'] = [str(st) for st in stateStack]
        df_stack['Input'] = [str(tk) for tk in contentTokens]
        df_stack['Action'] = [desc if not pd.isna(desc) else 'Error!']
        print(tabulate.tabulate(df_stack, headers='keys', tablefmt='psql'))

        if pd.isna(action) or action is None:
            print('\033[91m', 'Reject!', '\033[0m')
            raise Exception('Error!, not accepted')
        if action[0] == 'S':
            stateStack.append(action[1])
            contentTokens.pop(0)
        elif action[0] == 'R':
            prod: Tuple[str, int] = action[1]

            for _ in range(prod[1]):
                stateStack.pop()

            stateOn = stateStack[-1]
            A = prod[0]
            newAction, desc = reader.obtainAction(stateOn, A)
            if newAction is None or pd.isna(newAction):
                raise Exception('Action not found in', stateOn, A)
            stateStack.append(newAction[1])
        elif action[0] == 'A':
            break

    print('\033[92m','Accepted!', '\033[0m')

    return True


if __name__ == '__main__':
    source_file = '.\yapar\slr-2.yalp'
    output_file = '.\yapar_scanner\scan_yapar2_ext.pkl'  

    # Lectura de Yapar y Creacion de Automata SLR
    content = reader(source_file)
    Yapar = YaParReader(content)
    Yapar.obtain_productions()
    Yapar.generating_lr()
    Yapar.graph_lr0()
    print(Yapar)
    tableSlr = Yapar.get_slr_table()

    # Simular la lógica de exportar el objeto a un archivo pickle
    file_name = output_file if output_file else source_file.split('.')[0] + '.pickle'
    with open(file_name, 'wb') as file_pickle:
        pickle.dump(tableSlr, file_pickle)

    print(f'File {file_name} created')

    # Simular la lógica de leer el archivo pickle
    with open(file_name, 'rb') as file_pickle:
        tableSlr2 = pickle.load(file_pickle)
