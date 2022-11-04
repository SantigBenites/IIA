# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 11:34:03 2021

@author: santi
"""

from searchPlus import *
from utils import *
from EstadoSetas import *

def main():
    p = ProblemaSetas()
    print(p.initial)
    print(p.actions(p.initial))
    s1 = p.result(p.initial,6)
    print(s1)

class ProblemaSetas(Problem) :
    
    def __init__(self,initial = EstadoSetas(["e","e","e","d","d","d","d"]),goal=[EstadoSetas(["e","d","e","d","e","d","d"]),EstadoSetas(["d","e","d","e","d","e","d"])]) :
        """ Basta invocar o construtor de Problem com os dois argumentos initial e goal."""
        super().__init__(initial,goal)

    
    def actions(self,estado) :
        """ 5 acções: 1, 2, 3, 4 e 5.
            A acção 1 corresponde a inverter as setas de índices 0 e 1 da lista
            A acção 5 coorresponde a inverter as setas de índices 4 e 5, as últimas duas """
        accoes = list(range(len(self.initial.setas)))
        
        return accoes 

    def result(self,estado,acao) :
        """ Basta-nos invocar o método inverte definido na classe EstadoSetas. 
            No caso de a acção não ser reconhecida imprime mensagem de erro e devolve None"""
        if acao in self.actions(estado) :
          resultante = estado.inverte(acao)
        else :
            raise "Há aqui qualquer coisa mal>> acao não reconhecida"
 
        return resultante 
    
if __name__ == "__main__":
    main()