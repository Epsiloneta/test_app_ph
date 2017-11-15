 
import numpy as np 
import networkx as nx 
import pickle as pk 

M = np.random.random((100, 100))*5
for i in range(100):
    for j in range(i,100):
        M[j,i] = M[i,j]
        if(i==j):
            M[i,i]=0

g = nx.Graph(M)

np.savetxt('test1.txt',M,delimiter=',')
np.savetxt('test1.csv',M,delimiter=',')
np.save('test1.npy',M)
nx.write_gpickle(g, 'test1.gpickle')


