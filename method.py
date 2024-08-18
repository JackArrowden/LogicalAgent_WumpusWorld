from Constants import *

def getNextDir(curDir, listDir, x, y):
    numSteps = [5, 5, 5, 5]
    coorDir = {
        0: (x + 1, y) if x != 9 else None,
        1: (x, y + 1) if y != 9 else None,
        2: (x - 1, y) if x != 0 else None,
        3: (x, y - 1) if y != 0 else None
    }
    for i in range(4):
        if coorDir[i] is not None and coorDir[i] in listDir:
            numSteps[i] = (i - curDir) % 4
    
    while 3 in numSteps:
        numSteps[numSteps.index(3)] = 1.5
    
    choosenOne = numSteps.index(min(numSteps))

    listActions = []
    if numSteps[choosenOne] == 1:
        listActions = ['turn right']
    elif numSteps[choosenOne] == 2:
        listActions = ['turn right', 'turn right']
    elif numSteps[choosenOne] == 1.5:
        listActions = ['turn left']
    
    if numSteps[choosenOne] != 5:
        listActions.append('move forward')
    
    return coorDir[choosenOne] if numSteps[choosenOne] != 5 else None, listActions

def to_1D(x, y):
    return x * 10 + y + 1

def valid_cell(x, y):
    return 0 <= x < 10 and 0 <= y < 10

def adj_cell(x, y):
    for delta in Constants.DELTA:
        new_x = x + delta[0]
        new_y = y + delta[1]
        if valid_cell(new_x, new_y):
            yield tuple([new_x, new_y])

def is_element(percept, element):
    return element <= percept < element + 100

def is_signal_percept(predict):
    return (is_element(predict, Constants.BREEZE) or 
            is_element(predict, Constants.WHIFF) or 
            is_element(predict, Constants.STENCH) or 
            is_element(predict, Constants.GLOW))

def stench_infer_exist_wumpus_clause(x, y):
    clause = []
    clause.extend(element_clause(x, y, Constants.STENCH, True))
    clause.extend(element_clause(x, y, Constants.RELIABLE_S, True))
    for cell in adj_cell(x, y):
        clause.extend(element_clause(cell[0], cell[1], Constants.WUMPUS))
    return tuple(clause)

def breeze_infer_exist_pit_clause(x, y):
    clause = []
    clause.extend(element_clause(x, y, Constants.BREEZE, True))
    for cell in adj_cell(x, y):
        clause.extend(element_clause(cell[0], cell[1], Constants.PIT))
    return tuple(clause)

def glow_infer_exist_heal_clause(x, y):
    clause = []
    clause.extend(element_clause(x, y, Constants.GLOW, True))
    clause.extend(element_clause(x, y, Constants.RELIABLE, True))
    for cell in adj_cell(x, y):
        clause.extend(element_clause(cell[0], cell[1], Constants.HEAL))
    return tuple(clause)

def whiff_infer_exist_gas_clause(x, y):
    clause = []
    clause.extend(element_clause(x, y, Constants.WHIFF, True))
    for cell in adj_cell(x, y):
        clause.extend(element_clause(cell[0], cell[1], Constants.GAS))
    return tuple(clause)

def element_clause(x, y, element, is_not = False):
    signal = -1 if is_not else 1
    return tuple([signal * (to_1D(x, y) + element)])

def exist_element_clause(x, y, element):
    clause = []
    for new_cell in adj_cell(x, y):
        clause.append(to_1D(new_cell[0], new_cell[1]) + element)
    return tuple(clause)

def standardize_clause(clause):
    """
    Standardizes a CNF clause.
    :param clause: A list of variables in the clause (positive or negative integers).
    :return: The standardized clause as a sorted list of unique integers.
    """

    temp_clause = set(clause)
    std_clause = {*{}}
    for it in temp_clause:
        if -it in std_clause:
            std_clause.remove(-it)
        else:
            std_clause.add(it)
    return tuple(sorted(std_clause))

def PL_RESOLVE(clause_1, clause_2):
    new_clause = clause_1 + clause_2
    new_clause = standardize_clause(new_clause)
    return new_clause

def not_clauses(clauses):
    sentence = []
    for clause in clauses:
        sentence.append(not_clause(standardize_clause(clause)))
    
    result = sentence.pop()
    while len(sentence) > 0:
        new_clauses = []
        for clause_i in result:
            for clause_j in sentence[-1]:   
                new_clauses.append(PL_RESOLVE(clause_i, clause_j))
        result =  [list(item) for item in set(tuple(clause) for clause in new_clauses)]
        sentence.pop()    
    return result

def not_clause(clause):
    list_clause = []
    for e in clause:
        list_clause.append(tuple(-e))
    return list_clause

def is_empty(clause):
    return True if len(clause) == 0 else False 

