from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

a = np.arange(round(P[4,0]-500),round(P[4,0]+500))
b = np.arange(round(P[4,1]-500),round(P[4,1]+500))
teste = np.zeros([len(a),len(b)])
a, b = np.meshgrid(a,b)
v = np.zeros(4)

for k in range(1000):
    for j in range(1000):
        for i in range(4):
            v[i] = ((P[i,0]-a[k,j])**2 + (P[i,1]-b[k,j])**2)**0.5
        teste[k,j] = np.dot(v-dist[4,0:4],v-dist[4,0:4])
        
        
fig = plt.figure()
ax = fig.gca(projection='3d')

Axes3D.plot_surface(ax,a,b,teste)