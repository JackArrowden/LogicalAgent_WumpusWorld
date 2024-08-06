from clause import *
import copy

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

    def resolution(self, alpha):
        """
        try to prove KB entails alpha
        :param alpha: A list of clauses
        :return: True if KB entails alpha, False for unknown
        """
        alpha = standardize_clause(alpha)
        not_alpha = not_clauses(alpha)

        prev_clauses = set()

        cur_clauses = copy.deepcopy(self.KB)
        cur_clauses.update(not_alpha)
        new_clauses = set()
        while True:
            for clause_i in prev_clauses:
                for clause_j in cur_clauses:
                    resolvents = PL_RESOLVE(clause_i, clause_j)
                    if is_empty(resolvents):
                        return True
                    new_clauses.add(resolvents)

            for clause_i in cur_clauses:
                for clause_j in cur_clauses:
                    resolvents = PL_RESOLVE(clause_i, clause_j)
                    if is_empty(resolvents):
                        return True
                    new_clauses.add(resolvents)              

            prev_clauses.update(cur_clauses)
            if new_clauses.issubset(prev_clauses):
                return False
            cur_clauses = new_clauses

