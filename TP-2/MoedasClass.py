# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 12:48:28 2021

@author: santi
"""

class MoedasClass(Problem):
    
    def __init__(self,initial = 0 ,goal= 0):
        self.goal = goal
    
    def actions(self,estado):
        sucessores = [1,2,5,10,20,50]
        accoes = map(lambda x : "adicionar {}".format(estado,x),sucessores)
        return accoes 

    def result(self,estado,acao):
        return estado + acao
        
        
    