# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 16:57:46 2021

@author: Utilizador
"""

        
from Teste1 import *
from searchPlus import *
    

def distanceBetweenAndCenter(point,size):
    center = int(size/2)+1

    return abs(point[1] - center) + abs(point[2] - center)

def distanceBetweenAndCenterFour(point,size):
    center = int(size/2)+1
    points = [(center,center+1),(center+1,center),(center,center-1),(center-1,center)]
    dist = abs(point[1] - points[0][0]) + abs(point[2] - points[0][1])
    for x in points:
        if abs(point[1] - x[0]) + abs(point[2] - x[1]) <= dist:
            dist = abs(point[1] - x[0]) + abs(point[2] - x[1])
            
    return dist

def h(no):
    center = no.state.dim
    heuristica = 0;
    listOfPoints = list(no.state.robots)

    for x in listOfPoints:
        if x[0] == 'b':
            whiteRobot = x
    
    listOfPoints.remove(whiteRobot)
    
    heuristica += distanceBetweenAndCenter(whiteRobot,center)
    minDist = distanceBetweenAndCenterFour(listOfPoints[0],center);
    for point in listOfPoints:
        if(distanceBetweenAndCenterFour(point,center) <= minDist):
            minDist = distanceBetweenAndCenterFour(point,center)
            
    heuristica += minDist
    
    return heuristica
        

def aplicaAstar(p):
    solve = astar_search(PuzzleRobots(p.dim,p.initial), h)
    if solve != None:
        return (solve.path_cost,solve.solution())
    else :
        return None
    
#estadoInic = EstadoRobots(0, {('b',1,2), ('p',3,5), ('p',3,1),('p',4,2),('p',5,4), ('p',6,6)})
estadoInic = EstadoRobots(5, {('b',1,2), ('p',3,5), ('p',3,1),('p',4,2),('p',4,4), ('p',5,5)})
#estadoInic = EstadoRobots(3, {('b',1,2), ('p',1,1), ('p',3,2)})
PuzzleRobots.display(estadoInic,estadoInic)
print(h(Node(estadoInic)))
print( aplicaAstar(PuzzleRobots(5, estadoInic)))