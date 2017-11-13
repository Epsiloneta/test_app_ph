import sys
import os
computer = os.getlogin()
import pickle as pk
import networkx as nx
import numpy as np
import pylab as plt
import scipy.io
import timeit
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
data_path = '/home/epsilon/Dropbox/ISI_Esther/Easy_PH/tmp'
output_path = '/home/epsilon/Dropbox/ISI_Esther/Easy_PH/tmp'

def _to_lower_matrix(M,shape_M):
    """
    M: array (square matrix)
    shape_M: shape (int)
    from a full matrix create a lower matrix (without diagonal) and save it to a .txt file
    """
    ## lower matrix file
    file_input = open('tmp/input.txt','wb')

    for i in range(1,shape_M):
        for j in range(0,i):
            file_input.write(M[i,j]+',')
        file_input.write('\n')
    file_input.close()
    return()

def check_format_input(file_name,format_type=None):
    """
    open file given a format and create input file for Ripser
    """
    if(format_type == 'gpickle'):
        G = nx.read_gpickle(file_name)
        M = nx.adj_matrix(G).todense()
    if(format_type == 'npy'):
        M = np.load(file_name)
    if(format_type == 'csv' or format_type == 'txt'):
        # np.savetxt('a.txt',a,delimiter=',',newline='\n')
        # np.savetxt("a.csv", a, delimiter=",")
        np.loadtxt(file_name,delimiter=',')
    \todo try shape[0] == shape[1]
    shape_M = M.shape[0]
    _to_lower_matrix(M,shape_M)
    print 'input file created'
    return()    
    # print("--- %s seconds ---" % (timeit.default_timer() - start_time ))


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
    while(i+1<len(data) and stop == False):
        i = i+1
        l = data[i]
        d = l.strip()
        if(d[0]=='['):
            d = d[1:-1]
            if( d.split(',')[-1] != ' '):
                p = map(float, d.split(','))
                h_start.append(p[0]); h_end.append(p[1])
                i = i+1
            else:
                d = d.split(',')
                h_start.append(0); h_end.append(value_range[1])
                i = i+1
        else:
            stop = True
        
    return(h_start,h_end)


def read_ripser_output(output_path):
    """
    read ripser output file and convert to pandas. Save as csv
    """
    \todo add persistence by density (columns pers by threshold and column pers by dens)
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

        


# ----------------------------
## main ##
# -----------------------------
check_format_input(file_name,format_type=None)

exec_ripser(data_path,ripser_path,input_file='tmp/input.txt')

read_ripser_output(output_path)

### figures ##
# 

    # pers.sort()
    # ## Fig 1
    # fig = plt.figure(figsize=(12,5))
    # plt.subplot(1,2,1)
    # plt.plot(h_start,h_end,'bo',alpha=.3,label='dim %i'%dimH)
    # plt.title('PD H%i %i'%(dimH,ica_points))
    # plt.xlabel('birth')
    # plt.ylabel('death')
    # plt.xlim((min(h_start),max(h_end)))
    # plt.ylim((min(h_start),max(h_end)))
