import sys
import os
import pickle as pk
import networkx as nx
import numpy as np
import pandas as pd
import scipy.io
import timeit

## file with kernel similarity functions
from functions_kernel_similarity import *
## file with plots for kernel similarity
from functions_plot_kernel import plots_similarity_matrix, error_fill, plot_similarity_curve
## file with the main function to compute similarity
from main_function_similarity import main_function_similarity

##########################################################
userhome = os.path.expanduser('~')
ripser_path = os.path.join(userhome,'Software/ripser')
##########################################################

# columns birth, death and dimH
# .txt delimiter ',' or '\t'
## input 
# birth,death,persistence,dimH
# 0,1,1,0
# 0,1,1,0
# 0,1,1,0
# 0,1,1,0
# 0,1,1,0
# 0,1,1,0

# birth	death	persistence	dimH
# 0	1	1	0
# 0	1	1	0
# 0	1	1	0
# 0	1	1	0
# 0	1	1	0
# 0	1	1	0


# \TODO add new format, .txt with correct columns
data_path = '%s/Dropbox/ISI_Esther/Easy_PH/tmp/results/'%userhome
data_path = '%s/Dropbox/ISI_Esther/paolo_moretti_networks/generated_networks/results/'%userhome
format_type = 'csv'
dim=1
normalized = True
plots_on =True
sim_weighted = False # todo if true
output_path = None
sigma = None
delimiter = ','
# \TODO similarity weighted
sigma=[0.1,0.3,0.6,0.7]
main_function_similarity(data_path,format_type,output_path=None,sim_weighted=False,sigma=sigma,plots_on=True,normalized=normalized,dim=dim,vmax=True,delimiter=delimiter)


# sim_matrix_list  = [np.array([[  0.00000000e+00,   2.90358844e-04,   6.36422256e-03,
#           9.91411860e-03],
#        [  0.00000000e+00,   0.00000000e+00,   4.00827475e-02,
#           4.57490237e-04],
#        [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
#           7.80413372e-05],
#        [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
#           0.00000000e+00]]), np.array([[ 0.        ,  0.00769843,  0.01367194,  0.04855401],
#        [ 0.        ,  0.        ,  0.43573999,  0.00730463],
#        [ 0.        ,  0.        ,  0.        ,  0.00325588],
#        [ 0.        ,  0.        ,  0.        ,  0.        ]]), np.array([[ 0.        ,  0.01981697,  0.02192398,  0.14980117],
#        [ 0.        ,  0.        ,  0.7195568 ,  0.01705059],
#        [ 0.        ,  0.        ,  0.        ,  0.01169548],
#        [ 0.        ,  0.        ,  0.        ,  0.        ]]), np.array([[ 0.        ,  0.02334648,  0.02453401,  0.19059972],
#        [ 0.        ,  0.        ,  0.76619033,  0.01974415],
#        [ 0.        ,  0.        ,  0.        ,  0.01442011],
#        [ 0.        ,  0.        ,  0.        ,  0.        ]])]

# vmax = np.max([np.max(m) for m in sim_matrix_list])

# plt.figure(figsize=(12,17))
# num_plots = 4
# size = sim_matrix_list[0].shape[0]
# for i in range(1,num_plots+1):
#     ax = plt.subplot(2,2,i)
#     plt.imshow(sim_matrix_list[i-1],interpolation='None',vmin=0,vmax=vmax,cmap='Blues')
#     # plt.imshow(sim_matrix_list[i-1],interpolation='None',vmin=0,vmax=vmax)
#     plt.yticks([])
#     ax.plot([-0.5,3.5],[-0.5,3.5],'k')
#     plt.title('sigma 00000000000000 mean sim: , std sim: ')
# plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
# # plt.subplots_adjust(bottom=0.1, right=0., top=0.9)
# cax = plt.axes([0.85, 0.1, 0.075, 0.8])
# plt.colorbar(cax=cax)
# plt.suptitle('dgdgdhdhd')
# plt.show()

