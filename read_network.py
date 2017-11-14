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

# sys.path.append('/home/%s/Software/'%computer) #IMPORTANT (path holes)
# import Holes as ho
# sys.path.append('/home/%s/Dropbox/ISI_Esther/templates_stable/'%computer) #IMPORTANT (path holes)
# from functions_run_holes_complete import *
# from functions_plot_persistence_diagram import * 
# from functions_plots_summary_scaffs import * 


## INPUT: 
# weighted undirected network to do Clique Complex. Filtration will be on thresholds from 0 to n. Weights have a distance sense.
# distance matrix 


# create output for multiple files (TODO)

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

## parameters 
ripser_path = '/home/%s/Software/ripser'%computer
data_path = '/home/%s/Dropbox/ISI_Esther/Easy_PH/tmp'%computer
output_path = '/home/%s/Dropbox/ISI_Esther/Easy_PH/tmp'%computer


s = open(output_path+'/test.txt','wb')
s.write('dfhfhfhf\n')
s.close()

### figures ##

# ----------------------------
## main ##
# -----------------------------
file_name = 'test_M.txt'
M_max, M_shape = check_format_input(data_path,file_name,format_type='txt')

exec_ripser(data_path,ripser_path,input_file='input.txt')

read_ripser_output(output_path)

summary_output(output_path,M_shape,M_max)

## Plots ## 
## Plot input data
plot_input_data(data_path,file_name,output_path,format_type = 'txt',normalized=False)
plot_input_data(data_path,file_name,output_path,format_type = 'txt',normalized=True)
## Plot PDs
plot_PDs(output_path,M_max,normalized=False)
plot_PDs(output_path,M_max,normalized=True)
## Plot barcodes
plot_barcodes(output_path,M_max,normalized=True)
plot_barcodes(output_path,M_max,normalized=False)
# -----------------------------


## report: larger persistences, summary PH