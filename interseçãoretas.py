import numpy as np
from math import comb
import matplotlib.pyplot as plt
from random import randint

RAMDOM = True

def coordenadas():
    n = int(input("Quantos LEDs há?: "))

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

    return n, coordleds, coordsombra

def definirRetas(n, coordleds, coordsombra):
    m = np.zeros((n))
    b = np.zeros((n))

    for j in range(n):
        m[j] = (coordsombra[j][1] - coordleds[j][1]) / (coordsombra[j][0] - coordleds[j][0])  # m = (y2 - y1) / (x2 - x1)
        b[j] = coordleds[j][1] - m[j] * coordleds[j][0]  # y = mx + b (=) b = y - mx
        print("Função para o LED " + str(j + 1) + ": y = " + str(m[j]) + "x + " + str(b[j]))

    print(m)
    return m, b


def calcularIntersecao(n, m, b):
    #Dimensão das matrizes das coordenadas de interseção de 2 retas
    coordX = np.zeros((n-1,n))
    coordY = np.zeros((n-1,n))

    CoordX = 0
    CoordY = 0

    for i in range(n): #Obtenção das coordenadas x e y da interseção entre 2 retas
        for j in range(i+1,n):
            coordX[i][j] = (b[j] - b[i]) / (m[i] - m[j])  # y = m1*x+b1 & y = m2*x+b2 (=) m1*x+b1 = m2*x+b2 (=) x = (b2 - b1) / (m1 - m2)
            coordY[i][j] = (((m[i] * coordX[i][j]) + b[i]) + ((m[j] * coordX[i][j]) + b[j])) / 2  #Média: (y1 + y2) / 2
            print(str(i), str(j), coordX[i][j], coordY[i][j])

            CoordX += coordX[i][j]
            CoordY += coordY[i][j]

    intersecao = (CoordX/comb(n,2)), (CoordY/comb(n,2))  #Cálculo da média de todos os pontos obtidos (centróide)

    return intersecao, coordX, coordY


def PlotResult(n, m, b, intersecao, coordX, coordY):
    x = np.linspace(np.min(coordX) - 50,np.max(coordX) + 50)

    for i in range(0, n):
        y = m[i]*x + b[i]
        plt.plot(x, y)

    for i in range(n):
        for j in range(i+1,n):
            plt.plot(coordX[i][j], coordY[i][j], "go")

    plt.plot(intersecao[0], intersecao[1], "bo")

    plt.show()



def main():
    n, coordleds, coordsombra = coordenadas()
    m, b = definirRetas(n, coordleds, coordsombra)
    intersecao, coordX, coordY = calcularIntersecao(n, m, b)
    print("A coordenada de interseção das retas é: " + str(intersecao))
    PlotResult(n, m, b, intersecao, coordX, coordY)

main()
