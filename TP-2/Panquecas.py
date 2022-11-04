# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 16:25:16 2021

@author: santi
"""

from searchPlus import *

def main():
    p = PanquecasClass([9,8,7,6,5,4,3,2,1])
    print(p.initial)
    print(p.actions(p.initial))
    s1 = p.result(p.initial,6)
    print(s1)

class PanquecasClass(Problem):
    
    '''Estado vai ser a lista de panquecas ordenadas pelo tamanho 1 a mais pequena
    2 a segunda mais pequena etc...'''
    
    def __init__(self,initial = list(range(6))):
        super().__init__(initial,list(range(len(initial))))
    
    def actions(self,estado):
        sucessores = list(range(len(self.initial)))
        accoes = map(lambda x : "reverse as primeiras {} panquecas".format(estado,x),sucessores)
        return accoes 

    def result(self,estado,acao):
        temp = estado
        temp[acao:len(estado)] = temp[acao:len(estado)][::-1]
        return temp

    
if __name__ == "__main__":
    main()