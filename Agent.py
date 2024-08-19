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

        self.taken_actions = []

    def infer_update_KB(self, x, y):
        if self.percepts[(x, y)].have_stench():
            self.KB.add_clause(stench_infer_exist_wumpus_clause(x, y))
        elif self.percepts[(x, y)].have_no_stench():
            for cell in adj_cell(x, y):
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.WUMPUS, True))
        
        if self.percepts[(x, y)].have_breeze():
            self.KB.add_clause(breeze_infer_exist_pit_clause(x, y))
        elif self.percepts[(x, y)].have_no_breeze():
            for cell in adj_cell(x, y):
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.PIT, True))
        
        if self.percepts[(x, y)].have_whiff():
            self.KB.add_clause(whiff_infer_exist_gas_clause(x, y))
        elif self.percepts[(x, y)].have_no_whiff():
            for cell in adj_cell(x, y):
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.GAS, True))

        if self.percepts[(x, y)].have_glow():
            self.KB.add_clause(glow_infer_exist_heal_clause(x, y))
        elif self.percepts[(x, y)].have_no_glow():
            for cell in adj_cell(x, y):
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.HEAL, True))

        for percept in self.percepts[(x, y)].percepts:
            self.KB.update_unit_clause([percept])

    def update_KB(self):
        self.infer_update_KB(self.x, self.y)
        self.KB.update_unit_clause(element_clause(self.x, self.y, Constants.RELIABLE))

    def do(self, action):
        self.taken_actions.append(((self.x, self.y), action))
        self.environment.handleAction(action)
        if action == 'shoot':
            pass
        elif action == 'grab':
            if self.percepts[(self.x, self.y)].have_heal():
                self.num_healing_potion += 1
            elif not self.percepts[(self.x, self.y)].have_gold():
                raise ValueError('Invalid action, can not grab anything!')
        elif action == 'climb':
            if self.x != 0 or self.y != 0:
                raise ValueError('Invalid action, this position is not for climb!')
        elif action == 'move forward':
            self.x += Constants.DELTA[self.direction][0]
            self.y += Constants.DELTA[self.direction][1]
            if not valid_cell(self.x, self.y):
                raise ValueError('Invalid action, move out of map!')
            if [to_1D(self.x, self.y) + Constants.GAS] in self.environment.getPercept():
                self.health -= 1
            if self.health == 0:
                raise ValueError('zero health')
        elif action == 'turn left':
            self.direction = (self.direction + 3) % 4
        elif action == 'turn right':
            self.direction = (self.direction + 1) % 4
        elif action == 'heal':
            if self.num_healing_potion == 0:
                raise ValueError('Invalid action, there is no healing potion')   
            self.health = min(4, self.health + 1)
            self.num_healing_potion -= 1


    def infer(self, clause):
        if len(clause) == 1:
            x = (int(abs(clause[0]) - 1) % 100) // 10
            y = (int(abs(clause[0]) - 1) % 100) % 10
            # print(clause, x, y)
            if self.percepts[(x, y)].is_true(clause[0]):
                return True
        
        return self.KB.resolution(clause)

    def update_escaping_cost(self):
        frontier = PriorityQueue()
        start_cost = 2000
        for cell in adj_cell(self.x, self.y):
            if cell in self.cost_escaping:
                start_cost = min(start_cost, self.cost_escaping[cell] + self.percepts[cell].have_gas())
        
        if start_cost == 2000:
            start_cost = 0
        frontier.put((start_cost, self.x, self.y))
        self.cost_escaping[(self.x, self.y)] = start_cost

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

    def get_target_cell(self):
        problem = Problem(self.percepts, self.cost_escaping, self.candidate_cells, self.num_healing_potion + self.health, (self.x, self.y, self.direction))

        actions = UCS(problem)
        if actions is None:
            return False

        for action in actions:
            if action == 'move forward': 
                new_x = self.x + Constants.DELTA[self.direction][0]
                new_y = self.y + Constants.DELTA[self.direction][1]
                if not self.percepts[(new_x, new_y)].have_no_gas() and self.health == 1:
                    self.do('heal')
            self.do(action)
        self.candidate_cells.pop((self.x, self.y))

        return True

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
                self.percepts[(self.x, self.y)].update_percept(self.environment.getPercept())

                if self.percepts[(self.x, self.y)].have_no_stench():
                    kill_wumpus = True
                    break
                
                if self.environment.isSound:
                    kill_wumpus = True
                    continue
                else:
                    break

            if kill_wumpus:
                self.update_KB()
                change_x = self.x + Constants.DELTA[self.direction][0]
                change_y = self.y + Constants.DELTA[self.direction][1]
                self.percepts[(change_x, change_y)].update_percept(element_clause(change_x, change_y, Constants.WUMPUS, True))
                self.KB.update_unit_clause(element_clause(change_x, change_y, Constants.WUMPUS, True))
                for cell in adj_cell(change_x, change_y):
                    if self.percepts[cell].check_visited() and (cell[0] != self.x or cell[1] != self.y):
                        self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.RELIABLE, True))
                        candidate = Constants.CERTAINLY_GAS if self.percepts[cell].have_gas() else Constants.NORMAL
                        candidate = sum_cost(candidate, Constants.VERIFY)
                        self.candidate_cells[cell] = candidate 

            if self.percepts[(self.x, self.y)].have_no_stench():
                for cell in list_cells:
                    self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.WUMPUS, True))
                    self.percepts[cell].update_percept(element_clause(cell[0], cell[1], Constants.WUMPUS, True))
                return

    def analyze(self):
        unexpand_adj_cells = []
        for cell in adj_cell(self.x, self.y):
            if not self.percepts[cell].check_visited():
                unexpand_adj_cells.append(cell)

        # get all cell that we can infer it doesn't have pit
        valid_unexpand_cells = []
        for cell in unexpand_adj_cells:
            clause = element_clause(cell[0], cell[1], Constants.PIT, True)
            if self.infer(clause):
                self.percepts[cell].update_percept(clause)
                self.KB.update_unit_clause(clause)
                valid_unexpand_cells.append(cell)
                continue
            clause = element_clause(cell[0], cell[1], Constants.PIT)
            if self.infer(clause):
                self.percepts[cell].update_percept(clause)
                self.KB.update_unit_clause(clause)

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
            candidate = (0, 0)
            if self.infer(element_clause(cell[0], cell[1], Constants.HEAL)):
                candidate = sum_cost(candidate, Constants.CERTAINLY_HEAL)
                # print(cell, 'have_heal')
            elif self.infer(element_clause(cell[0], cell[1], Constants.HEAL, True)):
                self.percepts[cell].update_percept(element_clause(cell[0], cell[1], Constants.HEAL, True))
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.HEAL, True))
                # print(cell, 'no have heal')
            else:
                candidate = sum_cost(candidate, Constants.ABLE_HEAL)
                # print(cell, 'may be have heal')

            if self.infer(element_clause(cell[0], cell[1], Constants.GAS)):
                candidate = sum_cost(candidate, Constants.CERTAINLY_GAS)
                self.percepts[cell].update_percept(element_clause(cell[0], cell[1], Constants.GAS))
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.GAS))
                # print(cell, 'have gas')
            elif self.infer(element_clause(cell[0], cell[1], Constants.GAS, True)):
                self.percepts[cell].update_percept(element_clause(cell[0], cell[1], Constants.GAS, True))
                self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.GAS, True))
                # print(cell, 'have no gas')            
            else:
                candidate = sum_cost(candidate, Constants.ABLE_GAS)
                # print(cell, 'may be have gas')

            self.candidate_cells[cell] = candidate

    def init(self, program: Program):
        self.direction = 0
        self.x = 0
        self.y = 0
        self.health = 4
        self.num_healing_potion = 0

        self.KB = KnowledgeBase()
        self.percepts = {}
        for x in range(10):
            for y in range(10):
                self.percepts[(x, y)] = CellPercept(x, y)
        self.cost_escaping = dict()
        self.candidate_cells = dict()

        self.taken_actions = []

        self.environment = program
        self.percepts[(self.x, self.y)].update_percept(self.environment.getPercept())
        self.percepts[(self.x, self.y)].update_visited()
        self.update_KB()
        self.update_escaping_cost()
        self.analyze()
        
    def explore_world(self):
        while True:
            if not self.get_target_cell():
                break
            self.percepts[(self.x, self.y)].update_visited()
            self.percepts[(self.x, self.y)].update_percept(self.environment.getPercept())
            if self.percepts[(self.x, self.y)].have_gold():
                self.do('grab')
            grab_heal = False
            if self.percepts[(self.x, self.y)].have_heal():
                self.do('grab')
                grab_heal = True
        
            self.percepts[(self.x, self.y)].update_percept(self.environment.getPercept())
            self.update_KB()
            if grab_heal:
                for cell in adj_cell(self.x, self.y):
                    if self.percepts[cell].check_visited():
                        self.KB.update_unit_clause(element_clause(cell[0], cell[1], Constants.RELIABLE, True))
                        candidate = Constants.CERTAINLY_GAS if self.percepts[cell].have_gas() else Constants.NORMAL
                        candidate = sum_cost(candidate, Constants.VERIFY)
                        self.candidate_cells[cell] = candidate 
            self.update_escaping_cost()
            self.analyze()

        self.candidate_cells.clear()
        self.candidate_cells[(0, 0)] = Constants.NORMAL
        self.get_target_cell()
        self.do('climb')
        return self.taken_actions


if __name__ == '__main__':
    program = Program('map_sample_multi_3.txt')
    agent = Agent()
    agent.init(program)
    action = agent.explore_world()
    print('-----------------')
    for x in action:
        print(x[0], x[1])