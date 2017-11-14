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
ripser_path = '/home/esther/Software/ripser'
data_path = '/home/%s/Dropbox/ISI_Esther/Easy_PH/tmp'%computer
output_path = '/home/%s/Dropbox/ISI_Esther/Easy_PH/tmp'%computer

def _to_lower_matrix(data_path,M,shape_M):
    """
    M: array (square matrix)
    shape_M: shape (int)
    from a full matrix create a lower matrix (without diagonal) and save it to a .txt file
    """
    ## lower matrix file
    file_input = open('%s/input.txt'%data_path,'wb')
    for i in range(1,shape_M):
        for j in range(0,i):
            file_input.write(str(M[i,j])+',')
        file_input.write('\n')
    file_input.close()
    return()

def check_format_input(data_path,file_name,format_type=None,return_M = False):
    """
    open file given a format and create input file for Ripser
    data_path : path of data to read
    file_name: name (with extension) of the file to read
    format_type = 'gpickle', 'npy', 'csv', 'txt'
    return_M = False (we do not return input data), True (we return input data)
    """
    if(format_type == 'gpickle'):
        G = nx.read_gpickle(data_path+'/'+file_name)
        M = nx.adj_matrix(G).todense()
    if(format_type == 'npy'):
        M = np.load(data_path+'/'+file_name)
    if(format_type == 'csv' or format_type == 'txt'):
        # np.savetxt('a.txt',a,delimiter=',',newline='\n')
        # np.savetxt("a.csv", a, delimiter=",")
        M = np.loadtxt(data_path+'/'+file_name,delimiter=',')
    # \todo try shape[0] == shape[1]
    shape_M = M.shape[0]
    _to_lower_matrix(data_path,M,shape_M)
    print 'input file created in %s/input.txt'%data_path
    if(return_M):
        return(np.max(M),M)    
    else:
        return(np.max(M))    
    return()



def exec_ripser(data_path,ripser_path,output_path=None,input_file='tmp/input.txt'):
    if(output_path == None): output_path = data_path
    ############# RIPSER ####################
    # high dimension
    ## execfile ripser (OUTPUT from ripser)
    # im = os.getcwd()
    os.chdir(ripser_path)
    start = timeit.default_timer() 
    os.system('./ripser --format lower-distance --dim 2 %s/%s > %s/output_ripser.txt'%(data_path,input_file,output_path))
    os.chdir(data_path)
    # os.chdir(im)
    stop = timeit.default_timer()
    print 'Ripser execution time '
    print stop - start 
    return()


def ripser_PDs_dim(data,dim=2):
    """
    max dim 2
    given data file from output ripser, read file to extract (b,d) points for a given dimension
    """
    h_start = []; h_end = []
    value_range = eval(data[1].rstrip().split(' ')[-1])
    i=0
    l = data[i]
    stop = False
    while(l.strip()[-2:] !='%i:'%dim):
        i = i+1
        l = data[i]
    i = i +1 
    while(i<len(data) and stop == False):
        l = data[i]
        d = l.strip()
        print d
        if(d[0]=='['):
            d = d[1:-1]
            if( d.split(',')[-1] != ' '):
                p = map(float, d.split(','))
                h_start.append(p[0]); h_end.append(p[1])
                i = i+1
            else:
                d = d.split(',')
                h_start.append(float(d[0])); h_end.append(value_range[1])
                i = i+1
        else:
            stop = True
        
    return(h_start,h_end)


def read_ripser_output(output_path):
    """
    read ripser output file and convert to pandas. Save as csv
    """
    # \todo add persistence by density (columns pers by threshold and column pers by dens)
    data = open('%s/output_ripser.txt'%output_path,'rb').readlines()
    value_range = eval(data[1].rstrip().split(' ')[-1])
    # dimH = 2
    holes = dict() ## save holes by dimension (birth, death, persistence)
    for dimH in [0,1,2]:
        h_start, h_end = ripser_PDs_dim(data,dim=dimH)
        pers = np.array(h_end)-np.array(h_start)
        d = pd.DataFrame()
        d['birth'] = h_start
        d['death'] = h_end
        d['persistence'] = pers
        d['dimH'] = dimH
        holes[dimH] = d 
    data_pds = pd.concat(holes.values())
    data_pds.to_csv('%s/outputs_PDS.csv'%output_path) ## save pandas file with PDs for dim 0,1,2
    return()

def summary_output(data_pds):
    data = pd.read_csv(output_path+'/outputs_PDS.csv',index_col = 0) ## index_col to avoid generate a new indexed column
    data_ripser = open('%s/output_ripser.txt'%output_path,'rb').readlines()
    value_range = eval(data_ripser[1].rstrip().split(' ')[-1])
    summary_file = open(output_data+'/summary.txt','wb')
    summary_file.write('Number of nodes/points:%i\n'%M_shape)
    summary_file.write('value range:[%f,%f]'%(value_range[0],value_range[1]))

    for i in range(3):
        summary_file.write('Detected %i dim holes: %i\n'%(i,len(data[data.dimH==i])))
    # for i in range(3):
    #     summary_file.write('%i dim holes <75\% persistence: %i\n'%(i,len(data[data.dimH==i])))
    #     summary_file.write('%i dim holes <50\% persistence: %i\n'%(i,len(data[data.dimH==i])))
    #     summary_file.write('%i dim holes <25\% persistence: %i\n'%(i,len(data[data.dimH==i])))
    summary_file.close()
    print 'Summary file saved in %s/summary.txt'%output_path
    return()

### figures ##

# ----------------------------
## main ##
# -----------------------------
file_name = 'test_M.txt'
M_max = check_format_input(data_path,file_name,format_type='txt')

exec_ripser(data_path,ripser_path,input_file='input.txt')

read_ripser_output(output_path)


## Plots ## 
## Plot input data
plot_input_data(data_path,file_name,output_path,normalized=False)
plot_input_data(data_path,file_name,output_path,normalized=True)
## Plot PDs
plot_PDs(output_path,M_max,normalized=False,norm_by =None)
# plot_PDs(output_path,M_max,normalized=True,norm_by =None)
plot_PDs(output_path,M_max,normalized=True,norm_by ='max_M')
plot_PDs(output_path,M_max,normalized=True,norm_by ='max_bydim')
## Plot barcodes
plot_barcodes(output_path,M_max,normalized=True,norm_by ='max_bydim')
plot_barcodes(output_path,M_max,normalized=True,norm_by ='max_M')
plot_barcodes(output_path,M_max,normalized=False)
# -----------------------------


## report: larger persistences, summary PH