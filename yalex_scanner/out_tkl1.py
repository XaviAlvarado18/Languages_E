from typing import *


import argparse
parser = argparse.ArgumentParser(description='Simulate a machine')
parser.add_argument('source', help='Source file')
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
        



g2 = State('g2')
g1 = State('g1')
f1 = State('f1')
h4 = State('h4')
h3 = State('h3')
h2 = State('h2')
h1 = State('h1')
e1 = State('e1')
d1 = State('d1')
c1 = State('c1')
b1 = State('b1')
a1 = State('a1')
a0 = State('a0')
a0.add_transition(32, a1)
a0.add_transition(9, a1)
a0.add_transition(10, a1)
a0.add_transition(65, b1)
a0.add_transition(66, b1)
a0.add_transition(67, b1)
a0.add_transition(68, b1)
a0.add_transition(69, b1)
a0.add_transition(70, b1)
a0.add_transition(71, b1)
a0.add_transition(72, b1)
a0.add_transition(73, b1)
a0.add_transition(74, b1)
a0.add_transition(75, b1)
a0.add_transition(76, b1)
a0.add_transition(77, b1)
a0.add_transition(78, b1)
a0.add_transition(79, b1)
a0.add_transition(80, b1)
a0.add_transition(81, b1)
a0.add_transition(82, b1)
a0.add_transition(83, b1)
a0.add_transition(84, b1)
a0.add_transition(85, b1)
a0.add_transition(86, b1)
a0.add_transition(87, b1)
a0.add_transition(88, b1)
a0.add_transition(89, b1)
a0.add_transition(90, b1)
a0.add_transition(97, b1)
a0.add_transition(98, b1)
a0.add_transition(99, b1)
a0.add_transition(100, b1)
a0.add_transition(101, b1)
a0.add_transition(102, b1)
a0.add_transition(103, b1)
a0.add_transition(104, b1)
a0.add_transition(105, b1)
a0.add_transition(106, b1)
a0.add_transition(107, b1)
a0.add_transition(108, b1)
a0.add_transition(109, b1)
a0.add_transition(110, b1)
a0.add_transition(111, b1)
a0.add_transition(112, b1)
a0.add_transition(113, b1)
a0.add_transition(114, b1)
a0.add_transition(115, b1)
a0.add_transition(116, b1)
a0.add_transition(117, b1)
a0.add_transition(118, b1)
a0.add_transition(119, b1)
a0.add_transition(120, b1)
a0.add_transition(121, b1)
a0.add_transition(122, b1)
a0.add_transition(43, c1)
a0.add_transition(42, d1)
a0.add_transition(40, e1)
a0.add_transition(40, h1)
a0.add_transition(41, f1)
a0.add_transition(95, g1)

a1.isFinalState = True


def tk_a1(): 
	print('ws')


a1.token = tk_a1
a1.add_transition(32, a1)
a1.add_transition(9, a1)
a1.add_transition(10, a1)

b1.isFinalState = True


def tk_b1(): 
	with open('./tokens/tokens.txt', 'a') as archivo:
	      archivo.write("\nID")


b1.token = tk_b1
b1.add_transition(48, b1)
b1.add_transition(49, b1)
b1.add_transition(50, b1)
b1.add_transition(51, b1)
b1.add_transition(52, b1)
b1.add_transition(53, b1)
b1.add_transition(54, b1)
b1.add_transition(55, b1)
b1.add_transition(56, b1)
b1.add_transition(57, b1)
b1.add_transition(65, b1)
b1.add_transition(66, b1)
b1.add_transition(67, b1)
b1.add_transition(68, b1)
b1.add_transition(69, b1)
b1.add_transition(70, b1)
b1.add_transition(71, b1)
b1.add_transition(72, b1)
b1.add_transition(73, b1)
b1.add_transition(74, b1)
b1.add_transition(75, b1)
b1.add_transition(76, b1)
b1.add_transition(77, b1)
b1.add_transition(78, b1)
b1.add_transition(79, b1)
b1.add_transition(80, b1)
b1.add_transition(81, b1)
b1.add_transition(82, b1)
b1.add_transition(83, b1)
b1.add_transition(84, b1)
b1.add_transition(85, b1)
b1.add_transition(86, b1)
b1.add_transition(87, b1)
b1.add_transition(88, b1)
b1.add_transition(89, b1)
b1.add_transition(90, b1)
b1.add_transition(97, b1)
b1.add_transition(98, b1)
b1.add_transition(99, b1)
b1.add_transition(100, b1)
b1.add_transition(101, b1)
b1.add_transition(102, b1)
b1.add_transition(103, b1)
b1.add_transition(104, b1)
b1.add_transition(105, b1)
b1.add_transition(106, b1)
b1.add_transition(107, b1)
b1.add_transition(108, b1)
b1.add_transition(109, b1)
b1.add_transition(110, b1)
b1.add_transition(111, b1)
b1.add_transition(112, b1)
b1.add_transition(113, b1)
b1.add_transition(114, b1)
b1.add_transition(115, b1)
b1.add_transition(116, b1)
b1.add_transition(117, b1)
b1.add_transition(118, b1)
b1.add_transition(119, b1)
b1.add_transition(120, b1)
b1.add_transition(121, b1)
b1.add_transition(122, b1)

c1.isFinalState = True


def tk_c1(): 
	print("hola")


c1.token = tk_c1

d1.isFinalState = True


def tk_d1(): 
	print("Hola")


d1.token = tk_d1

e1.isFinalState = True


def tk_e1(): 
	with open('./tokens/tokens.txt', 'a') as archivo:
	      archivo.write("\n(")


e1.token = tk_e1

h1.add_transition(73, h2)

h2.add_transition(70, h3)

h3.add_transition(41, h4)

h4.isFinalState = True


def tk_h4(): 
	print("Esto es un if")


h4.token = tk_h4

f1.isFinalState = True


def tk_f1(): 
	with open('./tokens/tokens.txt', 'a') as archivo:
	      archivo.write("\n)")


f1.token = tk_f1

g1.add_transition(9, g1)
g1.add_transition(10, g1)
g1.add_transition(32, g1)
g1.add_transition(48, g1)
g1.add_transition(49, g1)
g1.add_transition(50, g1)
g1.add_transition(51, g1)
g1.add_transition(52, g1)
g1.add_transition(53, g1)
g1.add_transition(54, g1)
g1.add_transition(55, g1)
g1.add_transition(56, g1)
g1.add_transition(57, g1)
g1.add_transition(65, g1)
g1.add_transition(66, g1)
g1.add_transition(67, g1)
g1.add_transition(68, g1)
g1.add_transition(69, g1)
g1.add_transition(70, g1)
g1.add_transition(71, g1)
g1.add_transition(72, g1)
g1.add_transition(73, g1)
g1.add_transition(74, g1)
g1.add_transition(75, g1)
g1.add_transition(76, g1)
g1.add_transition(77, g1)
g1.add_transition(78, g1)
g1.add_transition(79, g1)
g1.add_transition(80, g1)
g1.add_transition(81, g1)
g1.add_transition(82, g1)
g1.add_transition(83, g1)
g1.add_transition(84, g1)
g1.add_transition(85, g1)
g1.add_transition(86, g1)
g1.add_transition(87, g1)
g1.add_transition(88, g1)
g1.add_transition(89, g1)
g1.add_transition(90, g1)
g1.add_transition(95, g2)
g1.add_transition(97, g1)
g1.add_transition(98, g1)
g1.add_transition(99, g1)
g1.add_transition(100, g1)
g1.add_transition(101, g1)
g1.add_transition(102, g1)
g1.add_transition(103, g1)
g1.add_transition(104, g1)
g1.add_transition(105, g1)
g1.add_transition(106, g1)
g1.add_transition(107, g1)
g1.add_transition(108, g1)
g1.add_transition(109, g1)
g1.add_transition(110, g1)
g1.add_transition(111, g1)
g1.add_transition(112, g1)
g1.add_transition(113, g1)
g1.add_transition(114, g1)
g1.add_transition(115, g1)
g1.add_transition(116, g1)
g1.add_transition(117, g1)
g1.add_transition(118, g1)
g1.add_transition(119, g1)
g1.add_transition(120, g1)
g1.add_transition(121, g1)
g1.add_transition(122, g1)

g2.isFinalState = True


def tk_g2(): 
	print("CADENA DE CARACTERES")


g2.token = tk_g2


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
        