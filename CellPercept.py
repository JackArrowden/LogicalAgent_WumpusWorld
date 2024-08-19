from Constants import *
from method import *

class CellPercept:
    def __init__(self, x, y, raw_percepts = None, is_visited = False):
        self.x = x
        self.y = y
        self.index = to_1D(x, y)
        self.is_visited = is_visited
        self.percepts = {*{}}
        if raw_percepts is not None:
            self.update_percept(raw_percepts)

    def update_percept(self, percept):
        if isinstance(percept, int):
            if -percept in self.percepts:
                self.percepts.remove(-percept)
            self.percepts.add(percept)
        elif isinstance(percept, tuple) and len(percept) == 1:
            if -percept[0] in self.percepts:
                self.percepts.remove(-percept[0])
            self.percepts.add(percept[0])
        elif isinstance(percept, list) and isinstance(percept[0], list):
            for p in percept:
                if -p[0] in self.percepts:
                    self.percepts.remove(-p[0])
                self.percepts.add(p[0])

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
    
    def have_glow(self):
        return (Constants.GLOW + self.index) in self.percepts

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
    
    def have_no_breeze(self):
        return -(Constants.BREEZE + self.index) in self.percepts
    
    def have_no_pit(self):
        return -(Constants.PIT + self.index) in self.percepts
    
    def have_no_stench(self):
        return -(Constants.STENCH + self.index) in self.percepts

    def have_no_gas(self):
        return -(Constants.GAS + self.index) in self.percepts
    
    def have_no_whiff(self):
        return -(Constants.WHIFF + self.index) in self.percepts
    
    def have_no_glow(self):
        return -(Constants.GLOW + self.index) in self.percepts
    
    def is_true(self, percept):
        return percept in self.percepts