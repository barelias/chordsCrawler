import numpy as np
import random

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

'''
    Funcao que le uma matriz de distancias e retorna um aproximacao do seu numero de dimensoes
'''
def dimentionalAnalizer (distances) :
    
    return 0

def moveBackGradient (consta, rand) :
    n = random.randrange(0, rand.shape[0], 1)
    gradient = np.zeros((rand.shape[1], 1))
    pot = lambda x : x**2
    for dim in range(0, rand.shape[1]) :
        norma = (np.sum(pot(getDistances(rand)[0] - getDistances(consta)[0])))**0.5
        p = np.zeros((rand.shape[0], 1))
        s = np.zeros((rand.shape[0], 1))
        for i in range (0, rand.shape[0]) :
            soma = np.sum(pot(rand[n] - rand[i]))
            p[i] = (soma)**0.5
        for i in range (0, rand.shape[0]) :
            if not (p[i] == 0) :
                s[i] = ((p[i] - getDistances(consta)[n][i]) * (1/(p[i]**0.5)) * (rand[n][dim] - rand[i][dim]))
            else :
                s[i] = 0
        if not (norma == 0):
            gradient[dim] = ((1/norma)*np.sum(s))
    return gradient
'''
    Funcao que le uma matriz de pontos ndimensionais e retorna a matriz distancias
'''
def getDistances (point) :
    (x, y) = point.shape
    matrix = np.zeros((x, x))
    for i in range(0, x) :
        for j in range(0, x) :
            for k in range(0, y) :
                matrix[i][j] += (point[i][k] - point[j][k])**2
    return matrix

def initRand (dimentions, points) :
    poi = np.random.rand(points, dimentions)
    increase = lambda x : x * 10
    poi = increase(poi)
    return poi

plt.axis('auto')

while (True) :
    randNum = np.random.rand(2, 1)
    if (int(randNum[0] * 10) >= 2 and int(randNum[1] * 10) >= 2) :
        break

points = initRand (2, int(randNum[1] * 10)) # points = initRand (int(randNum[0] * 10), int(randNum[1] * 10)) 
print("DIMENSAO: ")
print(points.shape[1])
print("PONTOS: ")
print(points)
print("DISTANCIAS: ")
print(getDistances (points))
print("RAND POINTS: ")
rand = initRand (2, int(randNum[1] * 10)) # rand = initRand (int(randNum[0] * 10), int(randNum[1] * 10))
diference = sum(getDistances(points)-getDistances(rand))
print (rand)

x = []
y = []
for i in range(0, 1000) :
    v = moveBackGradient(points, rand)
    passo = lambda x : x*0.01
    for j in range(0, rand.shape[1]) :
        print ("ESTRESSE: ", v[j])
        rand[j] = rand[j] - passo(v[j])
    plt.plot(i, v[0][0])
print("PONTOS: ")
print (points)
print("APROXIMACAO: ")
print (rand)
print("MUDANCA NA DIFERENCA: ")
print(diference, "------", sum(getDistances(points)-getDistances(rand)))
plt.show()