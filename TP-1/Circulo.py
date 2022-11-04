# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:52:46 2021

@author: Utilizador
"""
import math

def main():
    circ = Circulo(2,4)
    print(Circulo.area(circ))

class Circulo():
    def __init__ (self, centro, raio):
        self.centro = centro
        self.raio = raio
        
    def diametro (self) :
        return self.raio *2
        
    def area (self) :
        return math.pi * (self.raio ** 2)

    
if __name__ == "__main__":
    main()
    