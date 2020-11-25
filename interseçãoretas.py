import numpy as np
from math import factorial, comb
# from scipy import ndimage
from itertools import combinations
import matplotlib.pyplot as plt 
from random import randint

RAMDOM = True

def coordenadas():
    n = int(input("Quantos LEDS há? "))

    #Dimensão das matrizes das coordenadas dos LEDs e das Sombras
    coordleds = np.zeros((n,2))
    coordsombra = np.zeros((n,2))

    #Obtenção das coordenadas dos LEDs e das respetivas sombras
    for i in range(n):
        if RAMDOM:
            coordleds[i][0] = randint(-1000, 1000)
            coordleds[i][1] = 0
        else:
            coordleds[i][0] = input("Qual a coordenada x do LED " + str(i+1) + "?: ")
            coordleds[i][1] = input("Qual a coordenada y do LED " + str(i+1) + "?: ")
        print("LED " + str(i+1) + ": ( " + str(coordleds[i][0]) + " , " + str(coordleds[i][1]) + " ) \n")

        if RAMDOM:
            coordsombra[i][0] = randint(-1000, 1000)
            coordsombra[i][1] = 1000
        else:
            coordsombra[i][0] = input("Qual é a coordenada x do ponto médio da sombra do LED " + str(i+1) + "?: ")
            coordsombra[i][1] = input("Qual é a coordenada y do ponto médio da sombra do LED " + str(i+1) + "?: ")
        print("Sombra do LED " + str(i+1) + ": ( " + str(coordsombra[i][0]) + " , " + str(coordsombra[i][1]) + ") \n")

    print("Coordenadas das LEDs:")
    print(str(coordleds) + "\n")
    print("Coordenadas das sombras: ")
    print(str(coordsombra) + "\n")

    return n, coordleds, coordsombra

def definirRetas(n, coordleds, coordsombra):
    m = np.zeros((n))
    b = np.zeros((n))

    for j in range(n):
        m[j] = (coordsombra[j][1] - coordleds[j][1]) / (coordsombra[j][0] - coordleds[j][0])  # m = (y2 - y1) / (x2 - x1)
        b[j] = coordleds[j][1] - m[j] * coordleds[j][0]  # y = mx + b (=) b = y - mx
        print("Função para o LED " + str(j + 1) + ": y = " + str(m[j]) + "x + " + str(b[j]))

    return m, b

def Combinacoes(m, b): #Retorna uma lista de todas as combinações para m e b
    comb_m = list(combinations(m,2))
    comb_b = list(combinations(b,2))
    print(comb_m)
    print(comb_b)

    return comb_m, comb_b


def calcularIntersecao(n, comb_m, comb_b):
    #Dimensão das matrizes das coordenadas de interseção de 2 retas
    coordX = np.zeros(comb(n,2))
    coordY = np.zeros(comb(n,2))

    for k in range(comb(n,2)): #Obtenção das coordenadas x e y da interseção entre 2 retas
        coordX[k] = (comb_b[k][1] - comb_b[k][0]) / (comb_m[k][0] - comb_m[k][1])  # y = m1*x+b1 & y = m2*x+b2 (=) m1*x+b1 = m2*x+b2 (=) x = (b2 - b1) / (m1 - m2)
        coordY[k] = (((comb_m[k][0] * coordX[k]) + comb_b[k][0]) + ((comb_m[k][1] * coordX[k]) + comb_b[k][1])) / 2  #Média: (y1 + y2) / 2
        print(coordX[k], coordY[k])
    intersecao_retas = ((sum(coordX)/comb(n,2)), (sum(coordY)/comb(n,2)))  #Cálculo da média de todos os pontos obtidos (centróide)

    return intersecao_retas, coordX, coordY

def PlotResult(n, m, b, intersecao, coordX, coordY):
    x = np.linspace(min(coordX),max(coordX))

    for i in range(0, n):
        y = m[i]*x + b[i]

        plt.plot(x, y)

    plt.plot(intersecao[0], intersecao[1], "bo")

    plt.plot(coordX, coordY, "go")

    plt.show()



def main():
    n, coordleds, coordsombra = coordenadas()
    m, b = definirRetas(n, coordleds, coordsombra)
    comb_m, comb_b = Combinacoes(m, b)
    intersecao_retas, coordX, coordY = calcularIntersecao(n, comb_m, comb_b)
    print("A coordenada de interseção das retas é: " + str(intersecao_retas))
    PlotResult(n, m, b, intersecao_retas, coordX, coordY)

main()