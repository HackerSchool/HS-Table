# -*- coding: utf-8 -*-

class Reta:
    def __init__(self,ponto,vetor,vetorp):
        self.vetor = vetor
        self.ponto = ponto
        self.vetorp = vetorp
    
    def printPonto (self):
        print (self.ponto)
        
    def printVetor (self):
        print (self.vetor)
    
    def printVetorp (self):
        print (self.vetorp)
    

def coordenadas():
    n= int(input("Quantos leds há? "))
    cleds = []
    csombra = []
    for i in range(n):
        cleds.append(input("Quais as coordenadas do led? x,y: ")) 
        csombra.append(input("Quais são as coordenadas do ponto médio da sombra? x,y: "))
    return cleds, csombra
    

def definirRetas(cleds,csombra):
    retas = []
    
    for i in range(len(cleds)):
       pl = cleds[i]
       xl,yl = (pl.split(","))
       ps = csombra[i]
       xs,ys = (ps.split(","))
       xs,ys,xl,yl = int(xs),int(ys),int(xl),int(yl)
       xv = xs-xl
       yv = ys-yl
       vetor = (xv,yv)
       ponto = (xl,yl)
       vetorp = (-yv,xv)
       retas.append(Reta(ponto,vetor,vetorp))
       
    return retas
       
def calcularIntersecao(retas):
    
    
    
    
    
       
def main():
   cleds, csombra = coordenadas()
   retas = definirRetas(cleds, csombra)

   
main()