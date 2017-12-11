## functions to compute PH using Ripser
import sys
import os
import pickle as pk
import networkx as nx
import numpy as np
import pandas as pd
import scipy.io
import timeit
from ripser_wrapper_lib import ripser_call

# \TODO ojuuuuuuuuuu q si tenim gpickle potser es una adjacency matrix!!! be careful!!!!! Potser hauriem d ficar l'opcio adj matrix i convertirla

def _to_lower_matrix(data_path,M,shape_M):
    """
    M: array (square matrix)
    shape_M: shape (int)
    from a full matrix create a lower matrix (without diagonal) and save it to a .txt file
    """
    ## lower matrix file
    file_input_path = os.path.join(data_path,'input.txt')
    print 'data path ', file_input_path
    file_input = open(file_input_path,'wb')
    for i in range(1,shape_M):
        for j in range(0,i):
            file_input.write(str(M[i,j])+',')
        file_input.write('\n')
    file_input.close()
    return()

def check_format_input(data_path,file_name,lower_matrix,upper_matrix,format_type=None,return_M = False,create_input_file=True):
    """
    open file given a format and create input file for Ripser
    data_path : path of data to read
    file_name: name (with extension) of the file to read
    format_type = 'gpickle', 'npy', 'csv', 'txt'
    return_M = False (we do not return input data), True (we return input data)
    """
    file_full_path = os.path.join(data_path,file_name)
    if(upper_matrix or lower_matrix):
        max_val = 0; shape_M = 1
        with open(file_full_path,'r') as f:
            for lin in f:
                shape_M = shape_M +1
                lin = lin.strip().split(',')
                if(lin[-1]==''):
                    lin = lin[:-1]
                aux = np.max(map(float,lin))
                if(aux > max_val):
                    max_val = aux
    else: ## create lower matrix
        if(format_type == 'gpickle'):
            G = nx.read_gpickle(file_full_path)
            M = nx.adj_matrix(G).todense()
        if(format_type == 'npy'):
            M = np.load(file_full_path)
        if(format_type == 'csv' or format_type == 'txt'):
            # np.savetxt('a.txt',a,delimiter=',',newline='\n')
            # np.savetxt("a.csv", a, delimiter=",")
            M = np.loadtxt(file_full_path,delimiter=',')
        shape_M = M.shape[0]
        if(shape_M != M.shape[1]):
            raise Exception('Data input is not a square matrix!!!')
        max_val = np.max(M)
        if(create_input_file):
            _to_lower_matrix(data_path,M,shape_M)
    if(return_M):
        return(max_val,M)    
    else:
        return(max_val,shape_M)  
    return()



def exec_ripser(data_path,output_path,max_dim,input_file='input.txt',format_file = 'lower-distance',threshold=None):
    """
    output_name = output name_ripser
    format_file = 'lower-distance', 'upper-distance'
    threshold: stop to compute (usually for input networks where you have added values in no-link relationship)
    """
    ############# RIPSER ####################
    # high dimension
    ## execfile ripser (OUTPUT from ripser)
    start = timeit.default_timer() 
    print 'input_file ',input_file
    input_file_full = os.path.join(data_path,input_file)
    output_file_full = os.path.join(output_path,'output_ripser.txt')

    if threshold is None:
        ripser_arguments = 'ripser --format %s --dim %i %s'%(format_file,max_dim,input_file_full)
    else:
        ripser_arguments = 'ripser --format %s --dim %i --threshold %f %s'%(format_file,max_dim,threshold,input_file_full)
    
    ripser_call(ripser_arguments.split(' '),output_file_full)
    #os.system(ripser_call) # OLD CALL BASED ON executable

    stop = timeit.default_timer()
    print 'Ripser execution time '
    print stop - start 
    input_file_path = os.path.join(data_path,'input.txt')
    if(os.path.isfile(input_file_path)):
        os.remove(input_file_path)  ## remove auxiliar file with lower matrix used as input for Ripser
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


def read_ripser_output(output_path,max_dim,output_name=None):
    """
    read ripser output file and convert to pandas. Save as csv
    max_dim: max homology dimension computed
    """
    # \todo add persistence by density (columns pers by threshold and column pers by dens) ## only needed if input weighted network
    output_file_path =os.path.join(output_path,'output_ripser.txt')
    data = open(output_file_path,'rb').readlines()
    value_range = eval(data[1].rstrip().split(' ')[-1])
    holes = dict() ## save holes by dimension (birth, death, persistence)
    for dimH in range(0,max_dim+1):#[0,1,2]:
        print 'dimH ', dimH
        h_start, h_end = ripser_PDs_dim(data,dim=dimH)
        pers = np.array(h_end)-np.array(h_start)
        d = pd.DataFrame()
        d['birth'] = h_start
        d['death'] = h_end
        d['persistence'] = pers
        d['dimH'] = dimH
        holes[dimH] = d 
    data_pds = pd.concat(holes.values())
    if(output_name!=None):
        output_file_path = os.path.join(output_path,'%s_PDS.csv'%output_name)
        data_pds.to_csv(output_file_path) ## save pandas file with PDs for dim 0,1,2
        print 'Saved results in %s'%(output_file_path)
    else:
        output_file_path = os.path.join(output_path,'outputs_PDS.csv')
        data_pds.to_csv(output_file_path) ## save pandas file with PDs for dim 0,1,2
        print 'Saved results in %s'%output_file_path
    return()

def summary_output(output_path,M_shape,M_max,max_dim,output_name=None):
    """
    Summary of data: number points / nodes, range values of data, summary holes of dim 0,1,2 and number of important (def important in 3 levels: 25,50,75) holes according its persistence
    outpath
    M_shape, M_max
    max_dim: max homology dimension computed
    """
    if(output_name!=None):
        data = pd.read_csv(os.path.join(output_path,'%s_PDS.csv'%output_name),
            index_col = 0) ## index_col to avoid generate a new indexed column
        summary_file = open(os.path.join(output_path,'%s_summary.txt'%output_name),'wb')
    else:
        data = pd.read_csv(os.path.join(output_path,'outputs_PDS.csv'),
            index_col = 0) ## index_col to avoid generate a new indexed column
        summary_file = open(os.path.join(output_path,'summary.txt'),'wb')
    output_ripser_file = os.path.join(output_path,'output_ripser.txt')
    data_ripser = open(output_ripser_file,'rb').readlines()
    value_range = eval(data_ripser[1].rstrip().split(' ')[-1])
    summary_file.write('Number of nodes/points:%i\n'%M_shape)
    summary_file.write('value range:[%f,%f]\n'%(value_range[0],value_range[1]))

    for i in range(max_dim+1):
        summary_file.write('Detected %i dim holes: %i\n'%(i,len(data[data.dimH==i])))
    summary_file.write('---------------------------------------------------\n')
    for i in range(max_dim+1):
        v = data[data.dimH==i].persistence.values
        num_significant_75 = sum(v>M_max*.75)
        num_significant_50 = sum(v>M_max*.5)
        num_significant_25 = sum(v>M_max*.25)
        summary_file.write('%i dim holes greater 75%% across time persistence: %i\n'%(i,num_significant_75))
        summary_file.write('%i dim holes greater 50%% across time persistence: %i\n'%(i,num_significant_50))
        summary_file.write('%i dim holes greater 25%% across time persistence: %i\n'%(i,num_significant_25))
        summary_file.write('---------------------------------------------------\n')
    summary_file.close()
    if(output_name!=None):
        print 'Summary file saved in %s'%os.path.join(output_path,'%s_summary.csv'%output_name)
    else:
        print 'Summary file saved in %s'%os.path.join(output_path,'summary.csv')
    os.remove(output_ripser_file) ## remove file generated by Ripser
    return()