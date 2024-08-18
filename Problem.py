from typing import Optional
from Constants import Constants
from queue import PriorityQueue
from method import *
import math

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
    def __init__(self, state: State, parent: Optional['Node'] = None, action = None, path_cost: tuple = (0, 0)):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost[0] < other.path_cost[0] or (self.path_cost[0] == other.path_cost[0] and self.path_cost[1] < other.path_cost[1])

class Problem:
    def __init__(self, percepts, escaping_cost, start_list, max_heal, goal):
        self.percepts = percepts
        self.escaping_cost = escaping_cost 
        self.start = start_list
        self.goal = goal
        self.max_heal = max_heal

    def is_goal(self, current) -> bool:
        return current.x == self.goal[0] and current.y == self.goal[1] and current.direct == self.goal[2]
    
    def is_goal_cell(self, current) -> bool:
        return current.x == self.goal[0] and current.y == self.goal[1]
    
    def is_gas_cell(self, current) -> bool:
        return self.percepts[(current.x, current.y)].have_gas()
    
    def init(self):
        for start_cell, cost in self.start.items():
            start_cost = list(cost)
            if start_cell in self.escaping_cost:
                start_cost[0] += self.escaping_cost[start_cell]
            else:
                return_cost = 2000
                for cell in adj_cell(start_cell[0], start_cell[1]):
                    if cell in self.escaping_cost:
                        return_cost = min(return_cost, self.escaping_cost[cell] + self.percepts[cell].have_gas())
                start_cost[0] += return_cost
            for direct in range(4):
                yield tuple(start_cost), State(start_cell[0], start_cell[1], direct)

    def ACTIONS(self, current: State) -> list:
        actions = ['turn left', 'turn right']
        
        visual_direct = (current.direct + 2) % 4
        new_x = current.x + Constants.DELTA[visual_direct][0]
        new_y = current.y + Constants.DELTA[visual_direct][1]
        if valid_cell(new_x, new_y) and self.percepts[(new_x, new_y)].check_visited(): 
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
            new_x += Constants.DELTA[(current.direct + 2) % 4][0]
            new_y += Constants.DELTA[(current.direct + 2) % 4][1]

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

            cost = sum_cost(node.path_cost, self.ACTION_COST(cur_state, action, next_state))
            if math.ceil(cost[0]) >= self.max_heal:
                continue
            yield Node(next_state, node, action, cost)

def UCS(problem: Problem):
    frontier = PriorityQueue()
    reached = dict()
    for cost, state in problem.init():
        node = Node(state, None, None, cost)
        frontier.put((cost, node))
        reached[state] = node
    while not frontier.empty():
        cost, node = frontier.get()

        if reached[node.state].path_cost != cost:
            continue

        if problem.is_goal(node.state):
            return trace(node)
        
        for child in problem.EXPAND(node):
            if child.state not in reached or child.path_cost < reached[child.state].path_cost:
                reached[child.state] = child
                frontier.put((child.path_cost, child))
    return None


def sum_cost(cost1, cost2):
    if len(cost1) != len(cost2):
        raise ValueError("Hai tuple phải có cùng độ dài.")
    
    return tuple(a + b for a, b in zip(cost1, cost2))

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