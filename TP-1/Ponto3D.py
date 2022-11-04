# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 16:43:58 2021

@author: Utilizador
"""
import math

def main():
    pointA = Ponto3D( 3, 4 ,5)
    pointB = Ponto3D( 4, 6 ,4)
    print(Ponto3D.__str__(pointA))

class Ponto3D():
    def __init__ (self, x = 0, y = 0, z = 0):
        self.xCoordinate = x
        self.yCoordinate = y
        self.zCoordinate = z
        
    def __str__(self):
        return ("(" + str(self.xCoordinate) + "," + str(self.yCoordinate) + "," + str(self.zCoordinate) + ")")
        
    def distanciaOutroPonto (self, outroPonto):
        return math.sqrt((abs(self.xCoordinate -outroPonto.xCoordinate) ** 2) + (abs(self.yCoordinate -outroPonto.yCoordinate) ** 2)+ (abs(self.zCoordinate -outroPonto.zCoordinate) ** 2))
        
    def distanciaOrigem (self):
        return math.sqrt((abs(self.xCoordinate) ** 2) + (abs(self.yCoordinate)** 2) + (abs(self.zCoordinate) ** 2))
    
if __name__ == "__main__":
    main()
    