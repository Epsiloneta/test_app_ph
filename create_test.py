 
import numpy as np 
import networkx as nx 
import pickle as pk 

size = 20
M = np.random.random((size,size))*5
for i in range(size):
    for j in range(i,size):
        M[j,i] = M[i,j]
        if(i==j):
            M[i,i]=0

g = nx.Graph(M)

np.savetxt('test1.txt',M,delimiter=',')
np.savetxt('test1.csv',M,delimiter=',')
np.save('test1.npy',M)
nx.write_gpickle(g, 'test1.gpickle')

# save 2version network
nx.write_gpickle(g, 'test_nx_%s.gpickle'%nx.__version__)


## test esfera ##
# esfera a R^3 es fer X,Y,Z realitzacions d'una normal N(0,1)
# aleshores p = (x,y,z)/sqrt(x**2+y**2+z**2) és un punt sobre la esfera
size = 100


x = np.random.randn(size)
y = np.random.randn(size)
z = np.random.randn(size)

p = (x,y,z)/np.sqrt(x**2+y**2+z**2)

from scipy.spatial.distance import pdist
# An m by n array of m original observations in an n-dimensional space.
Y = pdist(p.transpose(), 'euclidean')
M = np.zeros((size,size))
k=0
for i in range(size):
    for j in range(i+1,size):
        M[i,j] = Y[k]
        M[j,i] = Y[k]
        k = k+1
np.savetxt('test_esfera_%i.txt'%size,M,delimiter=',')

import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(p[0], p[1], zs=p[2])
plt.show()

#### create networks (unweighted) ### 
size = 200
M = np.random.random((size,size))
for i in range(size):
    for j in range(i,size):
        if(i==j):
            M[i,i]=0
        else:
            if(M[i,j]>=.5):
                M[j,i] = 1
                M[i,j] = 1
            else:
                M[j,i] = 100
                M[i,j] = 100


np.savetxt('test_adj_matrix_to_dist_%i_th1.txt'%size,M,delimiter=',')
