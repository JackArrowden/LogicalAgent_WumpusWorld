from method import *
import copy
from pysat.solvers import Glucose3

class KnowledgeBase:
    def __init__(self): 
        self.KB = {*{}} # = set()
        set()

    def add_clause(self, clause):
        """
        Adds a standardized clause to the knowledge base if it is not already present.

        :param clause: A list of variables in the clause (positive or negative integers).
        :return: True if the clause was added to the KB, False otherwise.
        """
        clause = standardize_clause(clause)
        if clause not in self.KB:
            self.KB.add(clause)
            return True
        return False

    def del_clause(self, clause):
        """
        Removes a standardized clause from the knowledge base if it is present.

        :param clause: A list of variables in the clause (positive or negative integers).
        :return: True if the clause was removed from the KB, False otherwise.
        """
        clause = standardize_clause(clause)
        if clause in self.KB:
            self.KB.remove(clause)
            return True
        return False
    
    def update_unit_clause(self, clause):
        if len(clause) != 1:
            return False
        self.del_clause([-clause[0]])
        self.add_clause(clause)
        return True

    def resolution(self, alpha):
        """
        try to prove KB entails alpha
        :param alpha: A list of clause
        :return: True if KB entails alpha, False for unknown
        """
        alpha = standardize_clause(alpha)
        not_alpha = not_clause(alpha)

        g = Glucose3()
        clause_list = copy.deepcopy(self.KB)
        negative_alpha = not_alpha
        for it in clause_list:
            g.add_clause(it)
        for it in negative_alpha:
            g.add_clause(it)
        sol = g.solve()
        if sol:
            return False
        return True

if __name__ == '__main__':
    kb = KnowledgeBase()
    l = [(-101,), (1001,), (-111,), (-201,), (-211,), (-301,), (-401,), (-102,), (-202,), (-501,), (-411,), (-601,), (-701,), (-801,)]
    
    for x in l:
        kb.add_clause(x)
    print(kb.resolution((901,)))
    