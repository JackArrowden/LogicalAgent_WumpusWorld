from method import *
import copy
from pysat.solvers import Glucose3

class KnowledgeBase:
    def __init__(self): 
        self.KB = {*{}} # = set()
        set()

    def add_clause(self, clause):
        clause = standardize_clause(clause)
        if clause not in self.KB:
            self.KB.add(clause)
            return True
        return False

    def del_clause(self, clause):
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