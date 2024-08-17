from Constants import *
import copy
from method import *


class CellPercept:
    def __init__(self, x, y, raw_percepts, is_visited = False):
        self.x = x
        self.y = y
        self.index = to_1D(x, y)
        self.is_visited = is_visited
        self.percepts = {*{}}
        self.update_percept(raw_percepts)

    def update_percept(self, percept):
        if isinstance(percept, int):
            if -percept in self.percepts:
                self.percepts.remove(-percept)
            self.percepts.add(percept)
        elif isinstance(percept, list) or isinstance(percept, tuple):
            for p in percept:
                if -p in self.percepts:
                    self.percepts.remove(-p)
                self.percepts.add(p)

    def del_percept(self, percept):
        try:
            self.percepts.remove(percept)
            return True
        except Exception as e:
            return False
        
    def update_visited(self):
        self.is_visited = True

    def have_heal(self):
        return (Constants.HEAL + self.index) in self.percepts

    def have_gold(self):
        return (Constants.GOLD + self.index) in self.percepts

    def have_breeze(self):
        return (Constants.BREEZE + self.index) in self.percepts
    
    def have_stench(self):
        return (Constants.STENCH + self.index) in self.percepts

    def have_whiff(self):
        return (Constants.WHIFF + self.index) in self.percepts

    def have_gas(self):
        return (Constants.GAS + self.index) in self.percepts
    
    def have_pit(self):
        return (Constants.PIT + self.index) in self.percepts
    
    def have_wumpus(self):
        return (Constants.WUMPUS + self.index) in self.percepts
    
    def check_visited(self):
        return self.is_visited
    
    def have_no_wumpus(self):
        return -(Constants.WUMPUS + self.index) in self.percepts

    def have_no_pit(self):
        return -(Constants.PIT + self.index) in self.percepts
    
    def have_no_stench(self):
        return -(Constants.STENCH + self.index) in self.percepts

    def have_no_gas(self):
        return -(Constants.GAS + self.index) in self.percepts
    
    def have_no_whiff(self):
        return -(Constants.WHIFF + self.index) in self.percepts
    
    def is_true(self, percept):
        return percept in self.percepts
    
    # def to_clause(self):
    #     clauses = []
        
    #     for percept in self.percepts:
    #         clauses.append((tuple([])))
    #         if is_signal_percept(percept):
    #             clauses.append(signal_2_exist(self.x, self.y, percept))

    #     return clauses

