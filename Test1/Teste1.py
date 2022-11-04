# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 23:36:54 2021

@author: me
"""

from searchPlus import *

class EstadoRobots:
    """ Representação de um estado """
    
    def valido(dim, robots):
        """ função que permite verificar se um estado é válido"""
        if dim % 2 == 0 or dim <= 3:
            return False
        if len(robots) != dim + 1:
            return False
        numBrancos = 0
        numPretos = 0
        coords = set()
        for robot in robots:
            (c,linha,coluna) = robot
            if c == 'b':
                numBrancos += 1
            elif c == 'p':
                numPretos += 1
            else:
                return False
            if (linha,coluna) in coords:
                return False
            else:
                coords = coords.union({(linha,coluna)})
        return numBrancos == 1 and numPretos == dim
        
            
    def __init__(self, dim, robots):
        """ Cria um estado com dimensão dim e com os dim + 1 robôs representados no conjunto robots
            Cada elemento do conjunto robots é um triplo (cor, linha, coluna) onde:
                cor é 'b'(branco) ou 'p'(preto)
                linha é o número da linha onde o robô se encontra (entre 1 e dim)
                coluna é o número da coluna onde o robô se encontra (entre 1 e dim)
        """
        self.dim = dim
        self.robots = robots
        
    def __str__(self):
        grelha = "\n"
        for i in range(1, self.dim+1):
            for j in range(1, self.dim+1):
                if ('b',i,j) in self.robots:
                    grelha = grelha + "b"
                elif ('p',i,j) in self.robots:
                    grelha = grelha +"p"
                else:
                    grelha = grelha +"."
            grelha = grelha +"\n"
        return grelha
    
    def __eq__(self, estado):
        return isinstance(estado, EstadoRobots) and \
            self.dim == estado.dim and self.robots == estado.robots
    
    def __lt__(self, estado):
        return tuple(self.robots) < tuple(estado.robots)
    
    def __hash__(self):
        immutableState = tuple(self.robots)
        return immutableState.__hash__()
    
    def move(self, t, d):
        """ Produz um novo triplo resultante de mover o robô
            correspondente ao triplo t na direccao d
            Direcçoes: 'c'(cima),'b'(baixo),'e'(esquerda),'d'(direita)
            Caso o robô não exista no estado ou 
            o movimento não seja admissível, retorna None
        """
        if t not in self.robots:
            return None
        outrosRobots = self.robots.difference({t})
        coordOutrosRobots = set([(x,y) for (c,x,y) in outrosRobots])
        (c, i, j) = t
        if d == "d":
            if (i, j + 1) in coordOutrosRobots:
                return None
            for dj in range(2, self.dim+1-j):
                if (i,j+dj) in coordOutrosRobots:
                    return (c, i, j+dj-1)
        elif d == "e":
            if (i, j - 1) in coordOutrosRobots:
                return None
            for dj in range(-2, -j+2, -1):
                if (i,j+dj) in coordOutrosRobots:
                    return (c, i, j+dj+1)
        elif d == "b":
            if (i + 1, j) in coordOutrosRobots:
                return None
            for di in range(2, self.dim+1-i):
                if (i+di, j) in coordOutrosRobots:
                    return (c, i+di-1, j)
        elif d == "c":
            if (i - 1, j) in coordOutrosRobots:
                return None
            for di in range(-2, -i + 2, -1):
                if (i+di,j) in coordOutrosRobots:
                    return (c, i+di+1, j)
        return None
    
    def resultado(self, t, d):
        """Produz um novo estado resultante de mover o robô representado em
           t na direcção d
           caso o movimento seja inadmissível levanta uma excepção
        """
        novoT = self.move(t,d)
        if novoT:
            novoRobots = self.robots.difference({t}).union({novoT})
            return EstadoRobots(self.dim, novoRobots)
        else:
            raise Exception("Movimento inadmissível")
            
            
            
class PuzzleRobots(Problem):
    """Puzzle dos Robôs"""


    def __init__(self, dim, initial, goal=None):
        """Construtor:
            Assume que dim é impar > 3 e initial é instância válida do tipo EstadoRobots com a mesma dimensão"""
        self.dim = dim
        self.initial = initial
        self.goal = goal
    
            
    def actions(self, state):
        """ Assume que state é instância válida de EstadoRobots"""
        directions = ['b','c','e','d']
        actions = []
        for robot in state.robots:
            for d in directions:
                if state.move(robot,d):
                    actions.append((robot,d))
        return actions
        
    
    def result(self, state, action): 
        """ Assume que state é instância válida de EstadoRobots,
            que action é um par (robot, d) onde robot pertence a
            state.robots e d pertence a ['b','c','e','d'], e 
            que action é acção admissível em state
        """
        (robot,d) = action
        return state.resultado(robot,d)
        
    def goal_test(self,state):
        """ Verifica se o robô branco está na casa central da grelha"""
        centro = self.dim // 2 + 1
        return ('b', centro, centro) in state.robots
        
    def path_cost(self, cost,state,action,new_state):
        (robot, d) = action
        (cor,i1,j1) = robot
        (cor,i2,j2) = state.move(robot,d)
        if state.resultado(robot,d) != new_state:
            print("Algo está mal: estado resultante errado")
        if d in ['d', 'e']:
            return cost + abs(j2-j1)
        else:
            return cost + abs(i2-i1)
    
    def display(self, state):
        """ imprime o estado"""
        print(state)


    
        

        