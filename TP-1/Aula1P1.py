# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 11:43:20 2021

@author: santi
"""
def main():
    print(soma_digitos(le_inteiro()))
    
    

def sumOfMult(x) :
    x = input("escreva um valor sff")
    y = int(x)
    sum = 0
    for i in range(1,x):
        if i%3 == 0 or i%5 == 0:
            sum = sum + i
    print(sum)
    
def fib():
    sum = 0
    last = 1;
    secondLast = 1;
    temp = 0;
    while(last < 4000000):
        if last % 2 == 0:
            sum += last
        temp = last
        last = last + secondLast
        secondLast = temp
    print(sum)

def sumOfDigits():
    x = input("escreva um valor sff")
    try:
        val = sum([int(c) for c in x])
        print(val)
    except:
        print("Input Inválido:introduza um numero inteiro")

def le_inteiro():
    try:
        return int(input("escreva um valor sff"))
    except:
        print("Input Inválido:introduza um numero inteiro")

def soma_digitos(inteiro):
    
    num = inteiro
    sum = 0;
    
    while num > 0:
        remaidner = num % 10
        num = num / 10
        sum=int(sum+remaidner)
        
    return sum
        
        
        
def apaga_ocorrencias_noRange(tuplo, inteiro):
    x = ()
    for y in tuplo:
        if y != inteiro:
            x = x + (y,)
    print(x)

def apaga_ocorrencias_range(tuplo, inteiro):
    x = ()
    for y in range(len(tuplo)):
        if tuplo[y] != inteiro:
            x = x + (tuplo[y],)
    print(x)    
    
def apaga_ocorrencias_same(lista,inteiro):
    for y in lista:
        if y == inteiro:
            lista.remove(inteiro)
    print(lista)
    
def apaga_ocorrencias_different(lista,inteiro):    
    newList = []
    for y in lista:
        if y != inteiro:
            newList = newList + [y]
    print(newList)
    
    
if __name__ == "__main__":
    main()
    