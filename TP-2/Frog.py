# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 17:37:19 2021

@author: santi
"""
from searchPlus import *

def main():
    p = FrogProblem(['B','B','B','B','','R','R','R','R'])
    print(p.initial)
    print(p.actions(p.initial))
    s1 = p.result(p.initial,(5,4))
    print(s1)

class FrogProblem(Problem) :
    """ Sapos vermelhos sao representados por um R grande e Ras azuis por um B, espacos vazios por uma 
    String vazia, por fim um moviemnto e representado por um duplo com a localizacao do anfibio e o
    espaco para o qual queremos movimentar"""
    
    def __init__(self,initial = ['B','B','','R','R'],goal = None) :
        super().__init__(initial,goal)

    
    def actions(self,estado) :
        String = ""
        for bF in range(len(estado)):
            for wS in list(range(bF,len(estado))):
                if estado[bF] == 'B' and estado[wS] == '':
                    String += "BlueFrog in position " + str(bF) + " can move to whitespace in postion " + str(wS) + "\n"
        for rF in range(len(estado)):
            for wS in list(range(0,rF)):
                if estado[rF] == 'R' and estado[wS] == '':
                    String += "RedToad in position " + str(rF) + " can move to whitespace in postion " + str(wS) + "\n"
        return String 

    def result(self,estado,acao):
        newState = estado
        Anfibio = newState[acao[0]]
        Posicao = newState[acao[1]]
        if Posicao == '' and (Anfibio == "R" or Anfibio == "B") :
            if Anfibio == "R" and acao[0] > acao[1]:
                newState[acao[1]] = Anfibio
                newState[acao[0]] = ''
                return newState
            elif Anfibio == "B" and acao[0] < acao[1]:
                newState[acao[1]] = Anfibio
                newState[acao[0]] = ''
                return newState
            else:
                print("Input Inválido 2 :introduza um movemento valido")
                return newState
        else:
            print("Input Inválido 1 :introduza um movemento valido")
            return newState
        
    
if __name__ == "__main__":
    main()