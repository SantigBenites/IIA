# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 17:26:17 2021

@author: Utilizador
"""

from searchPlus import *
from utils import *

safe={'I':{'A':2,'B':5},'A':{'C':2,'D':4},'B':{'D':1,'F':5},'C':{},'D':{'C':3,'F':2},'F':{}}

class ProblemaGrafoCustos(Problem) :
    

    def __init__(self,initial = 'I', final = 'F',grafo = {'I':{'A':2,'B':5},
             'A':{'C':2,'D':4,'I':2},
             'B':{'D':1,'F':5,'I':5},
             'C':{},
             'D':{'C':3,'F':2},
             'F':{}}) :
        super().__init__(initial,final)
        self.grafo = grafo
        
    def actions(self,estado) :
        sucessores = self.grafo[estado].keys()  # métodos keys() devolve a lista das chaves do dicionário
        accoes = list(map(lambda x : "ir de {} para {}".format(estado,x),sucessores))
        return accoes

    def result(self, estado, accao) :
        """Assume-se que uma acção é da forma 'ir de X para Y'
        """
        return accao.split()[-1]
    
    def path_cost(self, c, state1, action, state2):
        return c + self.grafo[state1][state2]



def main():
    p = ProblemaGrafoCustos()
    path = PathCreate(p)
    print(path)
    print(path[-1].path_cost)
    print(p.initial)
    for node in path:
        print(node.action)
    for nodes in path[1].expand(p) :
        print(p.goal_test(nodes.state))
    
def PathCreate(p):
    
    queue = []
    queue.append(Node(p.initial))
    visited = []
    
    while queue:
        node = queue.pop()
        if p.goal_test(node.state):
            visited.append(node)
            return visited
        elif node not in visited:
            queue.extend(node.expand(p))
            visited.append(node)
    return None
    
def main2():
    ui=ProblemaGrafoCustos(grafo=safe)
    print(breadth_first_tree_echo_search(ui))

def breadth_first_tree_search(problem):
    """Search the shallowest nodes in the search tree first."""
    return tree_search(problem, FIFOQueue())


def depth_first_tree_search(problem):
    """Search the deepest nodes in the search tree first."""
    return tree_search(problem, Stack())

def tree_search(problem, frontier):
    frontier.append(Node(problem.initial))
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    return None

def breadth_first_tree_echo_search(problem):
    """Search the shallowest nodes in the search tree first."""
    return tree_echo_search(problem, FIFOQueue())


def depth_first_tree_echo_search(problem):
    """Search the deepest nodes in the search tree first."""
    return tree_echo_search(problem, Stack())


def tree_echo_search(problem, frontier):
    frontier.append(Node(problem.initial))
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        print(node.expand(problem))
    return None

def main3():
    ui = ProblemaGrafoCustos(grafo = safe)
    print(depth_first_tree_ord_search(ui))
    
def depth_first_tree_ord_search(problem):
    """Search the deepest nodes in the search tree first."""
    return tree_ord_search(problem, Stack())

def tree_ord_search(problem, frontier):
    frontier.append(Node(problem.initial))
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        frontier.reverse()
        print(frontier)
    return None

def main4():
    ui = ProblemaGrafoCustos(grafo = safe)
    print(depth_first_shuffle_tree_search(ui))
    
def depth_first_shuffle_tree_search(problem):
    """Search the deepest nodes in the search tree first."""
    return tree_shuffle_search(problem, Stack())

def tree_shuffle_search(problem, frontier):
    frontier.append(Node(problem.initial))
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
        random.shuffle(frontier)
        print(frontier)
    return None

            
            
if __name__ == "__main__":
    main4()