import sys
import os
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

# \TODO solve to put this here
# \TODO adapt '\' for windows
##########################################################
computer = os.getlogin()
ripser_path = '/home/%s/Software/ripser'%computer
##########################################################

def main_test(**kwarg):
    print kwarg

def check_and_prepare_variables(data_path,format_type,file_name,output_path):

    if(data_path==''):
        raise Exception('You need to select a Data folder')

    if(format_type=='txt-lowdist'):
        format_type = 'txt'
        lower_matrix = True
        upper_matrix= False
    elif(format_type=='txt-updist'):
        format_type = 'txt'
        upper_matrix= True
        lower_matrix = False
    else:
        upper_matrix= False
        lower_matrix = False

    if(file_name==''):
        file_name = None
    else:
        aux = file_name.split('.')[-1]
        if(aux!=format_type):
            raise Exception('Format input file does not correspond to File to analyse extension!')
        # ### \TODO windows!!!
        # if(os.name == 'nt'):
        #     file_name.split('/')
        #     print 'Im on windows'
        # elif(os.name == 'posix'):
        file_name = file_name.split('/')[-1]

    if(output_path == ''):
        output_path = None

    return(format_type,lower_matrix,upper_matrix,file_name,output_path,file_name)

def main_function(data_path,format_type,file_name=None,lower_matrix = False, upper_matrix = False, output_path=None,plots_on=True,normalized=False,max_dim=1):
    """
    data_path: folder path where data is. It will be used as folder where there are all files to compute PH
        Example: '/home/esther/Dropbox/ISI_Esther/Easy_PH/tmp'
    format_type: format of files to analyse: 'txt','npy','gpickle'
    
    OPTIONAL:
    file_name: in case that we only want to analyse one file pass its name (which is contained in the "data_path")
        Example: 'test_M.txt' (by default: None)
    output_path: path to save results, if None then output_path will be in data_path (by default: None)
    lower_matrix: (True or False), if the files are directly lower matrices just to pass to ripser (for large datasets)
    upper_matrix: (True or False), if the files are directly upper matrices just to pass to ripser (for large datasets)
    plots_on: True or False. Decide if you want to generate also plots of the results. It includes: plot input data, plot persistence diagrams depending max_dim choosen(dim 0,1,2), plot barcodes (dim 0,1,2). Persistent diagrams and barcodes are completelly equivalents. If True a folder plots will be generated in your output_path (by default: True)
    normalized: if you have plots_on = True, then you can choose if you want normalized or not plots (divided by the max value in the input data). Plots generated under normalized = True and normalized = False will be saved with different names, then you can do both options  (by default: False)
    max_dim: maximum dimension to compute homology (we only accept dim 0, 1, 2). Plots will be according max_dim chosen. (by default: 1)
    """
    ## create folder with results
    if(output_path == None): output_path = data_path
    output_path = '%s/results'%output_path
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ## Check just one active
    if(lower_matrix and upper_matrix):
        raise Exception('Only one True (lower_matrix or upper_matrix)')
    if((lower_matrix or upper_matrix) and format_type!='txt'):
        raise Exception('If (lower_matrix or upper_matrix) format file must be txt')
    ## Check if compute on only one file or on every file in the folder
    if(file_name!=None):
        ## Check input and read it
        M_max, M_shape = check_format_input(data_path,file_name,lower_matrix,upper_matrix,format_type=format_type)
        ## Execfile Ripser (for dim 0,1,2) depending on upper / lower format if input matrix in this way
        if(upper_matrix or lower_matrix):
            if(upper_matrix):
                exec_ripser(data_path,ripser_path,output_path,max_dim,input_file=file_name,format_file='upper-distance')
            else:
                exec_ripser(data_path,ripser_path,output_path,max_dim,input_file=file_name,format_file='lower-distance')
        else: ## normal way
            exec_ripser(data_path,ripser_path,output_path,max_dim,input_file='input.txt')
        ## read output ripser and convert to a nicer output
        read_ripser_output(output_path,max_dim)
        ## create a summary of your data and results
        summary_output(output_path,M_shape,M_max,max_dim)
        #-----------------------------------------------------------
        ## Plots ## 
        if(plots_on):
            ## check or create folder for plots
            plots_folder = '%s/plots'%output_path
            if not os.path.exists(plots_folder):
                os.makedirs(plots_folder)
            if(normalized):
                if(upper_matrix+lower_matrix!=1):
                    ## Plot input data
                    plot_input_data(data_path,file_name,plots_folder,format_type,lower_matrix,upper_matrix,normalized=True)
                ## Plot PDs
                plot_PDs(output_path,M_max,max_dim,normalized=True)
                ## Plot barcodes
                plot_barcodes(output_path,M_max,max_dim,normalized=True)
            else:
                if(upper_matrix+lower_matrix!=1):
                    ## Plot input data
                    plot_input_data(data_path,file_name,plots_folder,format_type,lower_matrix,upper_matrix,normalized=False)
                ## Plot PDs
                plot_PDs(output_path,M_max,max_dim,normalized=False)
                ## Plot barcodes
                plot_barcodes(output_path,M_max,max_dim,normalized=False)
        #-----------------------------------------------------------
    else:
        list_files = []  ## contains all desired files to compute PH (without extension)
        for f in os.listdir(data_path):
            if f.endswith('.%s'%format_type):
                list_files.append(f) ## add to summary
        print 'list_files to compute Persistent homology',list_files
        ## Plots ## 
        if(plots_on):
            ## check or create folder for plots
            plots_folder = '%s/plots'%output_path
            if not os.path.exists(plots_folder):
                os.makedirs(plots_folder)
        for file_name in list_files:
            ## Check input and read it
            M_max, M_shape = check_format_input(data_path,file_name,lower_matrix,upper_matrix,format_type=format_type)

            ## Execfile Ripser (for dim 0,1,2) depending on upper / lower format if input matrix in this way
            if(upper_matrix or lower_matrix):
                if(upper_matrix):
                    exec_ripser(data_path,ripser_path,output_path,max_dim,input_file=file_name,format_file='upper-distance')
                else:
                    exec_ripser(data_path,ripser_path,output_path,max_dim,input_file=file_name,format_file='lower-distance')
            else: ## normal way
                exec_ripser(data_path,ripser_path,output_path,max_dim,input_file='input.txt')

            ## read output ripser and convert to a nicer output
            output_name = file_name.split('.%s'%format_type)[0] ## name file withou extension
            read_ripser_output(output_path,max_dim,output_name=output_name)
            ## create a summary of your data and results
            summary_output(output_path,M_shape,M_max,max_dim,output_name=output_name)
            #-----------------------------------------------------------
            ## Plots ## 
            if(plots_on):
                if(normalized):
                    if(upper_matrix+lower_matrix!=1):
                        ## Plot input data
                        plot_input_data(data_path,file_name,plots_folder,format_type,lower_matrix,upper_matrix,normalized=True,output_name=output_name)
                    ## Plot PDs
                    plot_PDs(output_path,M_max,max_dim,normalized=True,output_name=output_name)
                    ## Plot barcodes
                    plot_barcodes(output_path,M_max,max_dim,normalized=True,output_name=output_name)
                else:
                    if(upper_matrix+lower_matrix!=1):
                        ## Plot input data
                        plot_input_data(data_path,file_name,plots_folder,format_type,lower_matrix,upper_matrix,normalized=False,output_name=output_name)
                    ## Plot PDs
                    plot_PDs(output_path,M_max,max_dim,normalized=False,output_name=output_name)
                    ## Plot barcodes
                    plot_barcodes(output_path,M_max,max_dim,normalized=False,output_name=output_name)
            #-----------------------------------------------------------
    return()
