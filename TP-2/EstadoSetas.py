# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 12:26:23 2021

@author: santi
"""

def main():
    x = EstadoSetas(["d","e","d","d","d","e","d","e"])
    print("Começamos com:",x)
    y = x.inverte(7)
    print("Primeira Inversao",y)
    z = y.inverte(2)
    print("Segunda Inversa",z)


class EstadoSetas :

    """Um estado do problema da inversao das setas
        Uma lista de 6 setas (e's ou d's), indicando para cada seta se está orientada
        para a esquerda para para a direita
        A ordem da esquerda para a direita corresponde às setas de cima para baixo
    """
    def __init__(self,setas) :
        """ Construtor: por omissão um estado corresponde ao estado inicial do problema"""
        self.setas = setas

        
    def flip(self,seta) :
        """ Inversão do sentido de uma seta: de e para d e de d para e"""
        if seta=="e":
            return "d"
        else:
            return "e"

    def inverte(self,n) :
        """ Inverte duas setas, na posição n e n+1. A primeira seta está na posição 0
            e para inverter a primeira e a segunda, de cima para baixo, implica n = 0.
            Gera uma nova lista.
        """
        if(n <= len(self.setas)-1):
            copye = []
            for i in range(len(self.setas)) :
                if i == n-1 or i == n :
                    copye.append(self.flip(self.setas[i]))
                else:
                    copye.append(self.setas[i])
            return EstadoSetas(copye)
        else:
            return EstadoSetas(self.setas)
    
    def __eq__(self,estado) :
        """Definir em que circunstância os dois estados são considerados iguais.
        Necessário para os algoritmos de procura em grafo.
        """
        return self.setas == estado.setas
        
    def __str__(self) :
        """ Cria uma string com a orientação das setas separadas pelo símbolos -.
            Esta é a string devolvida pelo método print"""
        return str("-".join(self.setas))
    
if __name__ == "__main__":
    main()