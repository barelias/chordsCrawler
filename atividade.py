import matplotlib.pyplot as plt
import numpy as np

passo = 0.00001
cid = 5
dim = 2
m = np.zeros([cid,cid])
k = np.arange(cid)
V = np.zeros(cid)

f = np.zeros([dim,cid-1])
    
dist = np.array([[   0, 205,3366,2580,3030],
                 [ 205,   0,3521,2783,3097],
                 [3366,3521,   0,2821,1630],
                 [2580,2783,2821,   0,3794],
                 [3030,3097,1630,3794,   0]])
    
#inicializar aleatoriamente 
P = np.random.rand(cid,dim)*1
        
for M in range(500000):
        
    #sorteio
    N = np.random.randint(cid)

    #Vetor de distâncias
    #for i in range(cid):
     #       V[i] = ((P[i,0]-P[N,0])**2 + (P[i,1]-P[N,1])**2)**0.5
    
    #f[0,:] carrega (xi - xn) e f[1,:] carrega (yi - yn)
    for i in range(dim):                    
        f[i,:] = P[k != N,i] - P[N,i]        
    g = (np.sum(f**2,axis=0))**0.5
    h = (g - dist[N,k != N])**2
    J = (np.sum(h))**0.5
    #Função de erro ^
    
    #Derivada (gradiente)
    alpha = np.sum((g-dist[N,k!=N])*g**-1*f*(-1),axis=1)
    dJ = J**-1*alpha

    for i in range(cid):
        for j in range(cid):
            m[i,j] = ((P[i,0]-P[j,0])**2 + (P[i,1]-P[j,1])**2)**0.5

    #Critério de parada
    if  (np.sum(((m-dist)/2)**2) <= 1000):
        break

    #Atualização das coordenadas do ponto sorteado
    P[N,:] = P[N,:] - alpha*passo

#Matriz de distâncias obtida
for i in range(cid):
    for j in range(cid):
        m[i,j] = ((P[i,0]-P[j,0])**2 + (P[i,1]-P[j,1])**2)**0.5

#Mostrar a diferença entre a matriz de erros e plotar os pontos
print(np.round(m-dist))
plt.plot(P[:,0],P[:,1],'.')