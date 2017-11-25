import sys
import os
computer = os.getlogin()
import pickle as pk
import networkx as nx
import numpy as np
import pylab as plt
import pandas as pd
import scipy.io
import timeit
import seaborn as sns

## file with PH functions
from functions_PH import *
## file with plot functions
from functions_plot import *
## file with main function
from function_main import *


## INPUT: 
# weighted undirected network to do Clique Complex. Filtration will be on thresholds from 0 to n. Weights have a distance sense.
# distance matrix 



## OUTPUT:
# PDs
# generators if you use Holes
# ------------------------------------------------------------
# Accepted formats: distance matrix (.txt columns splitted by spaces, rows splitted by \n and shape) (.pk array python, .gpickle network class), matlab matrix .mat

## Extras_
# Compute kernel similarity across different sigmas
# Compute weighted kernel similarity across different sigmas
# Compute Ricci-Curvature ?
# Plot: PDs, similarities, barcodes, scaffolds
# Plot: Ricci curvature distr and EMD given 2 distributions


# len(sys.argv)

# \todo: add more input type / format 

# ## parameters 
ripser_path = '/home/%s/Software/ripser'%computer
data_path = '/home/%s/Dropbox/ISI_Esther/Easy_PH/tmp'%computer
output_path = '/home/%s/Dropbox/ISI_Esther/Easy_PH/tmp'%computer
file_name = 'test1.txt'

max_dim = 1


# ---------------------------------------------------------------------------------------------------
# ## parameters Paolo Moretti data
# ---------------------------------------------------------------------------------------------------
data_folder = '/home/esther/Documents/data_paolo_moretti/redes_hmn2/'
# file_net = 'edgelist_n1024_s8_fl4'#n1024 number nodes

ripser_path = '/home/%s/Software/ripser'%computer
data_path = '%smatrices'%data_folder
file_name = 'edgelist_n1024_s8_fl4_matrix.txt'

max_dim = 1

# # ## one file
# main_function(data_path,'txt',max_dim=max_dim,file_name = file_name,lower_matrix = True, output_path=None,plots_on=True) 
# # ## folder files
# main_function(data_path,'txt',max_dim=max_dim,lower_matrix = True, output_path=None,plots_on=True) 


## ba matrices 
data_path = '/home/esther/Documents/data_paolo_moretti/ba_graphs/'
ripser_path = '/home/%s/Software/ripser'%computer
max_dim = 1
main_function(data_path,'gpickle',max_dim=max_dim, output_path=None,plots_on =False) 


# ---------------------------------------------------------------------------------------------------




# main_function(data_path,'txt',max_dim=max_dim,file_name = 'test_unweighted100.txt',output_path=None,plots_on=True) 

# main_function(data_path,'txt',max_dim=max_dim,file_name = file_name,output_path=None,plots_on=False) # ok
# main_function(data_path,'txt',max_dim=max_dim,file_name = file_name,output_path=None,plots_on=True) # ok 
# main_function(data_path,'txt',max_dim=max_dim,file_name = file_name,output_path=None,plots_on=True,normalized=True) # ok (with normalized and without, for each dimension)  

# main_function(data_path,'npy',output_path=None,plots_on=False) # ok 
# main_function(data_path,'gpickle',output_path=None,plots_on=True,normalized=True) # ok 


# main_function(data_path,'txt',file_name = file_name,output_path=None,plots_on=True,normalized=True) # ok
# main_function(data_path,'txt',file_name = file_name,output_path=None,plots_on=True) # ok
# main_function(data_path,'txt',output_path=None,plots_on=True) # ok 

# main_function(data_path,'txt',output_path=None,plots_on=True) # ok
# main_function(data_path,'txt',output_path=None,plots_on=True,normalized=True) # ok
# main_function(data_path,'txt',file_name=file_name,output_path=output_path,plots_on=True) # ok
# 
# main_function(data_path,'csv',file_name = file_name,output_path=None,plots_on=True) # ok


## test esfera - OK
# file_name = 'test_esfera.txt'
# main_function(data_path,'txt',file_name = file_name,output_path=None,plots_on=True,max_dim=2)
# file_name = 'test_esfera_192.txt'
# main_function(data_path,'txt',file_name = file_name,output_path=None,plots_on=True,max_dim=2)
# \TODO crear be CSV output sense columna extra ni numeracio (0,k)(0,l)

# -----------------------------

## OLD use of main: flux of the computation
# # ----------------------------
# ## main ##
# # -----------------------------
# ## Check input and read it
# M_max, M_shape = check_format_input(data_path,file_name,format_type='txt')
# ## Execfile Ripser (for dim 0,1,2)
# exec_ripser(data_path,ripser_path,input_file='input.txt')
# ## read output ripser and convert to a nicer output
# read_ripser_output(output_path)
# ## create a summary of your data and results
# summary_output(output_path,M_shape,M_max)

# ## Plots ## 
# ## Plot input data
# plot_input_data(data_path,file_name,output_path,format_type = 'txt',normalized=False)
# plot_input_data(data_path,file_name,output_path,format_type = 'txt',normalized=True)
# ## Plot PDs
# plot_PDs(output_path,M_max,normalized=False)
# plot_PDs(output_path,M_max,normalized=True)
# ## Plot barcodes
# plot_barcodes(output_path,M_max,normalized=True)
# plot_barcodes(output_path,M_max,normalized=False)
# # -----------------------------

