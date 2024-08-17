from typing import Optional
from Constants import Constants
from queue import PriorityQueue


class State:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direct = direction

    def __eq__(self, other: 'State') -> bool:
        return (self.x == other.x and 
                self.y == other.y and 
                self.direct == other.direct)
    
    def __ne__(self, other: 'State') -> bool:
        return not (self == other) 

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.direct))
    
    def __repr__(self) -> str:
        return f"State(x={self.x}, y={self.y})"

class Node:
    def __init__(self, state: State, parent: Optional['Node'] = None, action = None, path_cost = (0, 0)):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost[0] < other.path_cost[0] or (self.path_cost[0] == other.path_cost[0] and self.path_cost[1] < other.path_cost[1])

class Problem:
    def __init__(self, valid_cells, list_gas, start_list, goal):
        self.valid_cells = valid_cells
        self.gas = list_gas
        self.start = start_list
        self.goal = goal
    
    def is_goal(self, current) -> bool:
        return current.x == self.goal[0] and current.y == self.goal[1] and current.direct == self.goal[2]
    
    def is_goal_cell(self, current) -> bool:
        return current.x == self.goal[0] and current.y == self.goal[1]
    
    def is_gas_cell(self, current) -> bool:
        return (current.x, current.y) in self.gas
    
    def init(self) -> State:
        for s in self.start:
            if 

    def ACTIONS(self, current: State) -> list:
        actions = ['turn left', 'turn right']
        
        visual_direct = (current.direct + 2) % 4
        new_x = current.x + Constants.DELTA[visual_direct][0]
        new_y = current.y + Constants.DELTA[visual_direct][1]
        if (new_x, new_y) in self.valid_cells: 
            actions.append('move forward')

        return actions

    def RESULT(self, current: State, action: tuple[2]) -> State:
        new_x = current.x
        new_y = current.y
        new_direct = current.direct
        if action == 'turn left':
            new_direct = (new_direct + 1) % 4
        elif action == 'turn right':
            new_direct= (new_direct - 1) % 4
        elif action == 'move forward':
            new_x = new_x + Constants.DELTA[(current.direct + 2) % 4][0]
            new_y = new_y + Constants.DELTA[(current.direct + 2) % 4][1]

        return State(new_x, new_y, new_direct)

    def ACTION_COST(self, prev_state: State, action, cur_state: State):
        cost = [0, 1]

        if not self.is_goal_cell(cur_state) and self.is_gas_cell(cur_state) and (cur_state.x != prev_state.x or cur_state.y != prev_state.y):
            cost[0] = 1

        return tuple(cost)

    def EXPAND(self, node: Node):
        cur_state = node.state

        for action in self.ACTIONS(cur_state):
            next_state = self.RESULT(cur_state, action)

            cost = node.path_cost + self.ACTION_COST(cur_state, action, next_state)
            yield Node(next_state, node, action, cost)

def UCS(problem: Problem):
    frontier = PriorityQueue()
    reached = dict()
    for state, cost in problem.init():
        frontier.put(Node(state, None, None, cost))
        reached[state] = node()
    while not frontier.empty():
        cost, node = frontier.get()

        if reached[node.state] != cost:
            continue

        if problem.is_goal(node):
            return cost, trace(node)

        for child in problem.EXPAND(node):
            if not child.state in reached or child < reached[child.state]:
                reached[child.state] = child
                frontier.put((child.path_cost, child))


    return None


def sum_cost(cost1, cost2):
    if len(cost1) != len(cost2):
        raise ValueError("Hai tuple phải có cùng độ dài.")
    
    return tuple(a + b for a, b in zip(cost1, cost2))

def max_cost(cost1, cost2):

def trace(last_node):
    if last_node is None:
        return -1
    path = []
    node = last_node
    while node is not None:
        if node.action is not None:
            path.append(node.action)
        node = node.parent
    return path