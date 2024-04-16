import string
from tools.Classes_ import State, Node
from typing import *
import os
import importlib.util
from tools.draw import *
from queue import Queue
from tools.Tree_ import *
from tools.reader import *
from tools.transformer import *
import threading


def minimizeAFD(states2: Dict[str or int, State], alpha: Set[int or str], id_:str = 'Q'):
    initSt = states2['q0']
    initState = tuple([states2[x] for x in states2 if not states2[x].isFinalState])
    finalState = tuple([states2[x] for x in states2 if states2[x].isFinalState])
    minimized_states: Dict[str, Tuple[State, ...]] = {id_+'0': initState, id_+'1': finalState}

    not_toDo = True
    while not_toDo:
        evaluated = 1
        new_minimized_states: Dict[str, Tuple[State, ...]] = dict()
        for subStates in minimized_states:
            transitionsDict: Dict[str, Set[State]] = dict()
            for minState in minimized_states[subStates]:
                transitions: List[Tuple[str, str]] = []
                for letter in alpha:
                    if len(minState.getStates(letter)) <= 0:
                        pass
                    else:
                        newState = minState.getStates(letter).copy().pop()
                        for subStates2 in minimized_states:
                            if newState in minimized_states[subStates2]:
                                transition: Tuple[str, str] = (subStates2, letter)
                                transitions.append(transition)

                tupleTransitions: str = str(transitions)
                if tupleTransitions in transitionsDict:
                    transitionsDict[tupleTransitions].add(minState)
                else:
                    transitionsDict[tupleTransitions] = {minState}

            for transition_ in transitionsDict:
                if initSt in transitionsDict[transition_]:
                    new_minimized_states[id_ + str(0)] = tuple(transitionsDict[transition_])
                    continue
                new_minimized_states[id_ + str(evaluated)] = tuple(transitionsDict[transition_])
                evaluated += 1

        if len(new_minimized_states) == len(minimized_states):
            not_toDo = False
        else:
            minimized_states = new_minimized_states


    newMin_States: Dict[str, State] = dict()
    initial = ''
    for subStates in minimized_states:
        index = subStates

        if states2['q0'] in minimized_states[subStates]:
            initial = index
        newMin_States[index] = State(index)

        for minState in minimized_states[subStates]:
            if minState.isFinalState:
                newMin_States[index].isFinalState = True
                newMin_States[index].token = minState.token
                break

    for subStates in minimized_states:
        index = subStates
        tryState: State = tuple(minimized_states[subStates])[0]
        newMinState: State = newMin_States[index]

        for letter in alpha:
            if len(tryState.getStates(letter)) <= 0:
                continue

            tranState = tryState.getStates(letter).copy().pop()
            for subStates2 in minimized_states:
                if tranState in minimized_states[subStates2]:
                    newMinState.add_transition(letter, newMin_States[subStates2])
                    break

    newMin_States[initial].value = id_+'0'

    return newMin_States, newMin_States[initial]

def create_mach(token, regex, count, resultQueue: Queue, TreeQueue: Queue):
    parsed: List[List[str or int]] = transformsChar(regex)
    accepted: List[List[str or int]] = validate(parsed)
    alphabets: List[Set[int]] = extract_alphabet(accepted)
    formatted: List[List[str or int]] = format_regex(accepted)
    postfix: List[str or int] = translate_to_postfix(formatted)
    tree = make_direct_tree(postfix[0], token=token)
    TreeQueue.put(tree)
    direct = make_direct_AFD(tree[0], tree[1], alphabets[0], token)
    minimize = minimizeAFD(direct[2], alphabets[0], id_=string.ascii_lowercase[count])
    resultQueue.put(minimize[1])

def make_direct_AFD(tree: Node, nodes: Dict[str or int, Node], alphaSet: Set[int], token: str = ''):
    alpha = list(alphaSet)

    states: Dict[Tuple[int or str, ...], State] = {tuple(tree.first_pos): State('q0')}
    toEvaluate: List[Tuple[int, ...]] = [tuple(tree.first_pos)]
    total_states: Dict[str, State] = dict()
    initSta: Tuple[int, ...] = tuple(tree.first_pos)
    total_states['q0'] = states[initSta]
    finalState: str = ''
    for state in nodes:
        if nodes[state].value == '#':
            finalState = state
            break
    gen = 1

    while len(toEvaluate) > 0:
        actualState: Tuple[int, ...] = toEvaluate.pop(0)

        for letter in alpha:
            nextState_st: Set[int] = set()
            for state in actualState:
                if nodes[state].value == letter:
                    nextState_st = nextState_st.union(nodes[state].follow_pos)

            if len(nextState_st) <= 0:
                continue
            nextState: Tuple[int, ...] = tuple(nextState_st)
            if nextState not in states:
                states[nextState] = State('q' + str(gen))
                total_states['q' + str(gen)] = states[nextState]
                if finalState in nextState_st:
                    states[nextState].isFinalState = True
                toEvaluate.append(nextState)
                gen += 1
            states[actualState].add_transition(letter, states[nextState])

    for state in states:
        if finalState in state:
            states[state].isFinalState = True
            states[state].token.add(token)

    return states, states[initSta], total_states

def prepareAFN(expressions: Dict[str, List[str]], showTree = False) -> State:
    initState: State or None = None
    cont = 0
    threads: List[threading.Thread] = []
    resultQueue = Queue()
    TreeQueue = Queue()
    for token, regex in expressions.items():
        for i in range(len(regex)):
            t = threading.Thread(target=create_mach, args=(token, [regex[i]], cont, resultQueue, TreeQueue))
            threads.append(t)
            t.start()
            cont += 1

    for t in threads:
        t.join()

    while not resultQueue.empty():
        mach = resultQueue.get()
        if initState is None:
            initState = mach
        else:
            initState.combine_States(mach)

    iniTreeNode:Node = Node('Root')
    while not TreeQueue.empty():
        leftTree = TreeQueue.get()
        if iniTreeNode.left is None:
            iniTreeNode.left = leftTree[2]
            if iniTreeNode.right is None and not TreeQueue.empty():
                iniTreeNode.right = TreeQueue.get()[2]
                if TreeQueue.empty():
                    break
                newInitNode = Node('Root')
                newInitNode.left = iniTreeNode
                iniTreeNode = newInitNode
            continue
        else:
            iniTreeNode.right = leftTree[2]
            if TreeQueue.empty():
                break
            newInitNode = Node('Root')
            newInitNode.left = iniTreeNode
            iniTreeNode = newInitNode

    if showTree:
        draw_tree(iniTreeNode, 'default', useNum=True)
    initState.value = 'a0'
    return initState

def translateToCode(initState: State, isOut: bool = False, header='') -> str:
    code = ''
    setStates: Dict[str, State] = {initState.value: initState}

    def addState(state: State):
        for tran, states in state.transitions.items():
            for st in states:
                if st.value not in setStates:
                    setStates[st.value] = st
                    addState(st)

    addState(initState)

    for i, state in setStates.items():
        code = f"{i} = State('{i}')\n" + code
        if state.isFinalState:
            code += f"{i}.isFinalState = True\n"
        if len(state.token) > 0:
            if isOut:
                code += f"""\n\ndef tk_{i}(): \n"""
                for j in state.token:
                    code += f"\t{j}\n"
                code += f"\n\n{i}.token = tk_{i}\n"
            else:
                for j in state.token:
                    formatted_j = j.replace("'", r"\'")
                    code += f"{i}.addToken('{formatted_j}')\n"


        for tran, states in state.transitions.items():
            for st in states:
                code += f"{i}.add_transition({tran}, {st.value})\n"
        code += '\n'



    if isOut:
        code = """
class State:
    def __init__(self, value: str) -> None:
        self.value: str = value
        self.transitions: Dict[str or int, Set['State']] = {}
        self.isFinalState: bool = False
        self.numTrans: int = 0

    def add_transition(self, value: str or int, state: 'State') -> None:
        if value in self.transitions:
            self.transitions[value].add(state)
        else:
            self.transitions[value] = {state}

        self.numTrans += 1

    def getStates(self, transition_value) -> Set['State']:
        return self.transitions[transition_value] if transition_value in self.transitions else set()

    def __eq__(self, other):
        if isinstance(other, State):
            return (self.value, id(self)) == (other.value, id(self))
        return False

    def __hash__(self):
        return hash((self.value, id(self)))

    def getToken(self) -> str or None:
        return str(list(self.token)[0]) if len(self.token) > 0 else None

    def numberTransitions(self) -> int:
        return self.numTrans
        

\n\n""" + code

        code = """
import argparse
parser = argparse.ArgumentParser(description='Simulate a machine')
parser.add_argument('source', help='Source file')"""+header + code

        code = f"from typing import *\n\n" + code


        code += r"""
args = parser.parse_args()
fileToRead = args.source
def exclusiveSim(initState: State, string: str):
    string += ' '
    paths: List[List[State]] = [[initState]]
    listTextTuple: List[Tuple[str, str or int]] = []
    lastPathAccepted: List[Tuple[int, List, int]] = []

    chIndex = 0
    lasChIndex = 0

    while chIndex < len(string):
        ch = string[chIndex]
        char = ord(ch)
        newPaths: List[List[State]] = []

        for path in paths:
            evalState: State = path[-1]

            for st in evalState.getStates(char):
                newPath = path.copy()
                newPath.append(st)
                newPaths.append(newPath)

        if len(newPaths) == 0:
            if len(lastPathAccepted) == 0:
                textToAccept = string[lasChIndex:chIndex + 1]
                listTextTuple.append((textToAccept, 0 if len(textToAccept) == 0 or textToAccept == ' ' else 1))
                chIndex += 1
                lasChIndex = chIndex
                paths = [[initState]]
                continue

            lastChar, lastStateAccepted, _ = lastPathAccepted[0]
            textToAccept = string[lasChIndex:lastChar + 1]
            listTextTuple.append((textToAccept, lastStateAccepted[-1].token))
            lasChIndex = lastChar + 1
            chIndex = lastChar + 1
            paths = [[initState]]
            lastPathAccepted = []
            continue

        newLastPathAccepted = []

        for path in newPaths:
            if path[-1].isFinalState:
                newLastPathAccepted.append(
                    (chIndex, path, path[-1].value))

        if len(newLastPathAccepted) > 0:
            lastPathAccepted = sorted(newLastPathAccepted, key=lambda x: x[2])

        paths = newPaths
        chIndex += 1

    return listTextTuple


CYAN = '\033[96m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
REVERSE = '\033[7m'


if __name__ == '__main__':
    with open(fileToRead, 'r') as file:
        contents = file.read()

    print(YELLOW, 'Resultado:', RESET)
    tokens = exclusiveSim(a0, contents)
    for message, token in tokens:
        if token != 1 and token != 0:
            print(GREEN, message, RESET, '->')
            token()
        elif token == 1:
            print(RED, 'ERROR IN LINE:', message, RESET)
        """
    else:
        code = f"from Classes_ import State\n\n" + code
    return code


def import_module(file, regex, showTree=False):
    file = './authomata/' + file
    if os.path.isfile(file):
        import_module = file.split('.')[0]
        spec = importlib.util.spec_from_file_location(import_module, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        a0 = getattr(module, 'a0', None)
    else:
        a0 = prepareAFN(regex, showTree=showTree)
        code = translateToCode(a0)
        with open(file, 'w') as fileW:
            fileW.write(code)

    return a0