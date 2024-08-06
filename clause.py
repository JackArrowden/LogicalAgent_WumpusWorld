
def standardize_clause(clause):
    """
    Standardizes a CNF clause.
    :param clause: A list of variables in the clause (positive or negative integers).
    :return: The standardized clause as a sorted list of unique integers.
    """
    temp = set(clause)
    for it in temp:
        if -it in temp:
            temp.remove(it)
            temp.remove(-it)
    return sorted(list(temp))

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
        list_clause.append([-e])
    return list_clause

def is_empty(clause):
    return True if len(clause) == 0 else False 



if __name__ == '__main__':
    clause = [[1, -3], [4, 1]]
    result = not_clauses(clause)
    print(result)