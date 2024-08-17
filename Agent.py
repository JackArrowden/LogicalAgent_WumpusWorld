from Program import Program  
from KnowledgeBase import *
from method import *
from Constants import Constants 
from CellPercept import *
from queue import PriorityQueue, Queue
from Problem import *

class Agent:
    def __init__(self):
        self.direction = 0
        self.x = 0
        self.y = 0
        self.health = 4
        self.num_healing_potion = 0
        self.environment = None

        self.KB = KnowledgeBase()
        self.percepts = {}

        self.cost_escaping = dict()
        self.candidate_cells = dict()

    def infer_update_KB(self, x, y):
        if self.percepts[(x, y)].have_stench():
            self.KB.add_clause(stench_infer_exist_wumpus_clause(x, y))
        elif self.percepts[(x, y)].have_no_stench():
            for cell in adj_cell(x, y):
                self.KB.add_clause(element_clause(cell[0], cell[1], Constants.WUMPUS, True))
        
        if self.percepts[(x, y)].have_breeze():
            self.KB.add_clause(breeze_infer_exist_pit_clause(x, y))
        elif self.percepts[(x, y)].have_no_breeze():
            for cell in adj_cell(x, y):
                self.KB.add_clause(element_clause(cell[0], cell[1], Constants.PIT, True))
        
        if self.percepts[(x, y)].have_whiff():
            self.KB.add_clause(whiff_infer_exist_gas_clause(x, y))
        elif self.percepts[(x, y)].have_no_whiff():
            for cell in adj_cell(x, y):
                self.KB.add_clause(element_clause(x, y, Constants.GAS, True))

        if self.percepts[(x, y)].have_glow():
            self.KB.add_clause(glow_infer_exist_heal_clause(x, y))

        for percept in self.percepts[(x, y)]:
            self.KB.update_unit_clause([percept])

    def update_KB(self):
        self.infer_update_KB(self.x, self.y)
        self.KB.update_unit_clause(element_clause(self.x, self.y, Constants.RELIABLE))

    def do(self, action):
        if action == 'shoot':
            pass
        elif action == 'grab':
            if self.percepts[(self.x, self.y)].have_heal():
                self.num_healing_potion += 1
            elif not self.percepts[(self.x, self.y)].have_gold():
                raise ValueError('Invalaid action, can not grab anything!')
        elif action == 'climb':
            if self.x != 0 and self.y != 0:
                raise ValueError('Invalid action, this position is not for climb!')
        elif action == 'move forward':
            self.x += Constants.DELTA[self.direction][0]
            self.y += Constants.DELTA[self.direction][1]
            if not valid_cell(self.x, self.y):
                raise ValueError('Invalid action, move out of map!')
        elif action == 'turn left':
            self.direction = (self.direction + 3) % 4
        elif action == 'turn right':
            self.direction = (self.direction + 1) % 4
        elif action == 'heal':
            if self.num_healing_potion == 0:
                raise ValueError('Invalid action, there is no healing potion')   
            self.health = min(100, self.health + 25)
            self.num_healing_potion -= 1

        self.environment.handleAction(action)

    def infer(self, clauses):
        if len(clauses) == 1:
            x = ((clauses[0] - 1) % 100) / 10
            y = ((clauses[0] - 1) % 100) % 10
            if (x, y) in self.percepts and self.percepts[(x, y)].is_true(clauses[0]):
                return True
        
        return self.KB.resolution(clauses)

    def update_escaping_cost(self, x, y):
        frontier = PriorityQueue()
        start_cost = 2000
        for cell in adj_cell(x, y):
            if cell in self.cost_escaping:
                start_cost = min(start_cost, self.cost_escaping[cell] + self.percepts[cell].have_gas())
        
        if start_cost == 2000:
            start_cost = 0
        frontier.put((start_cost, x, y))
        self.cost_escaping[(x, y)] = start_cost


        while not frontier.empty():
            cost, x, y = frontier.get()

            if self.cost_escaping[(x, y)] != cost:
                continue

            for cell in adj_cell(x, y):
                if cell not in self.cost_escaping:
                    continue

                child_cost = self.cost_escaping[cell] + self.percepts[cell].have_gas()

                if self.cost_escaping[cell] > child_cost:
                    frontier.put((child_cost, cell[0], cell[1]))
                    self.cost_escaping[cell] = child_cost

    # def get_escaping_cost(self, x, y):

    def get_target_state(self):
        problem = Problem(self.percepts, self.candidate_cells, (self.x, self.y, self.direction))
        UCS(problem)

    def clear_wumpus(self, list_cells: list):
        n = len(list_cells)

        for _ in range(n):
            target_cell, actions = getNextDir(self.direction, list_cells, self.x, self.y)
            for action in actions:
                self.do(action)
            list_cells.remove(target_cell)

            kill_wumpus = False
            while True:
                self.do('shoot')
                percepts = self.environment.getPercept()
                self.percepts[(self.x, self.y)].update_percept(percepts)

                if self.percepts[(self.x, self.y)].have_no_stench():
                    kill_wumpus = True
                    break
                
                if self.environment.isSound:
                    kill_wumpus = True
                    continue

            if kill_wumpus:
                change_x = self.x + Constants.DELTA[self.direction][0]
                change_y = self.y + Constants.DELTA[self.direction][1]
                self.percepts[(change_x, change_y)].update_percept(element_clause(change_x, change_y, Constants.WUMPUS, True))
                self.update_KB(self.x, self.y)
                self.infer_update_KB(change_x, change_y)
                for cell in adj_cell(change_x, change_y):
                    if self.percepts[cell].check_visited() and cell[0] != self.x and cell[1] != self.y:
                        self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.RELIABLE, False))
                        candidate = Constants.CERTAINLY_GAS if self.percepts[cell].have_gas() else Constants.NORMAL
                        candidate = sum_cost(candidate, Constants.VERIFY)
                        self.candidate_cells[cell] = candidate 

            if self.percepts[(self.x, self.y)].have_no_stench():
                return

    def analyze(self):
        unexpand_adj_cells = []
        for cell in adj_cell(self.x, self.y):
            if cell not in self.percepts or not self.percepts[cell].check_visited():
                unexpand_adj_cells.append(cell)

        # get all cell that we can infer it doesn't have pit
        valid_unexpand_cells = []
        for cell in unexpand_adj_cells:
            clause = element_clause(cell[0], cell[1], Constants.PIT, True)
            if self.infer(clause):
                self.percepts[cell].update_percept(clause)
                self.KB.update_unit_clause(clause)
                valid_unexpand_cells.append(cell)

        # clear all wumpus
        wumpus_cells = []
        for cell in valid_unexpand_cells:
            clause = element_clause(cell[0], cell[1], Constants.WUMPUS, True)
            if not self.infer(clause):
                wumpus_cells.append(cell)
                continue
            self.percepts[cell].update_percept(clause)
            self.KB.update_unit_clause(clause)

        self.clear_wumpus(wumpus_cells)

        # insert all expand cells in to candidate list
        for cell in valid_unexpand_cells:
            candidate = (0, 0, 0)
            if self.infer(element_clause(cell[0], cell[1], Constants.HEAL)):
                candidate = sum_cost(candidate, Constants.CERTAINLY_HEAL)
            elif self.infer(element_clause(cell[0], cell[1], Constants.HEAL, True)):
                self.percepts[cell].update_percept(element_clause(cell[0], cell[1], Constants.HEAL, True))
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.HEAL, True))
            else:
                candidate = sum_cost(candidate, Constants.ABLE_HEAL)

            if self.infer(element_clause(cell[0], cell[1], Constants.GAS)):
                candidate = sum_cost(candidate, Constants.CERTAINLY_GAS)
                self.percepts[cell].update_percept(element_clause(cell[0], cell[1], Constants.GAS))
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.GAS))
            elif self.infer(element_clause(cell[0], cell[1], Constants.GAS, True)):
                self.percepts[cell].update_percept(element_clause(cell[0], cell[1], Constants.GAS, True))
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.GAS, True))
            else:
                candidate = sum_cost(candidate, Constants.ABLE_GAS)

            self.candidate_cells[cell] = candidate
            

    def init(self, program: Program):
        self.environment = program
        self.percepts[(self.x, self.y)] = CellPercept(self.x, self.y, self.environment.getPercept(), True)
        self.update_KB()
        self.analyze()
        
    def explore_world(self):
        while True:
            if not self.get_target_state():
                break
            
            self.percepts[(self.x, self.y)].update_percept(self.environment.getPercept())
            if self.percepts[(self.x, self.y)].have_gold():
                self.do('grab')
            if self.percepts[(self.x, self.y)].have_heal():
                self.do('grab')
                for cell in adj_cell(self.x, self.y):
                    if self.percepts[cell].check_visited():
                        candidate = Constants.CERTAINLY_GAS if self.percepts[cell].have_gas() else Constants.NORMAL
                        candidate = sum_cost(candidate, Constants.VERIFY)
                        self.candidate_cells[cell] = candidate 

            self.percepts[(self.x, self.y)].update_percept(self.environment.getPercept())
            self.analyze()

        self.candidate_cells.append((0, 0, 'climb'))
        self.get_target_state()
        self.do('climb')
        



