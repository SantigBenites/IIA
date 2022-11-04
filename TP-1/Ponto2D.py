# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:22:48 2021

@author: Utilizador
"""
import math

def main():
    pointA = Ponto2D( 3, 4 )
    pointB = Ponto2D( 4, 6 )
    print(Ponto2D.distanciaOrigem(pointA))
    
class Ponto2D(): 
    def __init__ (self, x = 0, y = 0):
        self.xCoordinate = x
        self.yCoordinate = y
        
    def __str__(self):
        return ("(" + str(self.xCoordinate) + "," + str(self.yCoordinate) + ")")
        
    def distanciaOutroPonto (self, outroPonto):
        return math.sqrt((abs(self.xCoordinate -outroPonto.xCoordinate) ** 2) + (abs(self.yCoordinate -outroPonto.yCoordinate) ** 2))
        
    def distanciaOrigem (self):
        return math.sqrt((abs(self.xCoordinate) ** 2) + (abs(self.yCoordinate)** 2))

if __name__ == "__main__":
    main()
    