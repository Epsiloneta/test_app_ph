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


# len(sys.argv)

## read a folder, read all files, number_them,
def main_function(data_path,format_type,file_name=None,output_path=None,plots_on=True,normalized=False):
    """
    data_path: foldar path where data is. It will be used as folder where are all files to compute PH
        Exemple: '/home/esther/Dropbox/ISI_Esther/Easy_PH/tmp'
    file_name: in case that we only want to analyse one file pass its name
        Exemple: 'test_M.txt'
    format_type: format of files to analyse: 'txt','npy','gpickle'
    output_path: path to save results, if None then output_path will be in data_path
    plots_on: True or False. Decide if you want to generate also plots of the results. It includes: plot input data, plot persistence diagrams (dim 0,1,2), plot barcodes (dim 0,1,2). Persistent diagrams and barcodes are completelly equivalents.
        If True a folder plots will be generated in your output_path
    normalized: if you have plots_on = True, then you can choose if you want normalized or not plots (divided by the max value in the input data)
    """
    ## create folder with results
    if(output_path == None): output_path = data_path
    output_path = '%s/results'%output_path
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    ## Check if compute on only one file or on every file in the folder
    if(file_name!=None):
        ## Check input and read it
        M_max, M_shape = check_format_input(data_path,file_name,format_type=format_type)
        ## Execfile Ripser (for dim 0,1,2)
        exec_ripser(data_path,ripser_path,output_path,input_file='input.txt')
        ## read output ripser and convert to a nicer output
        read_ripser_output(output_path)
        ## create a summary of your data and results
        summary_output(output_path,M_shape,M_max)
        #-----------------------------------------------------------
        ## Plots ## 
        if(plots_on):
            ## check or create folder for plots
            plots_folder = '%s/plots'%output_path
            if not os.path.exists(plots_folder):
                os.makedirs(plots_folder)
            if(normalized):
                ## Plot input data
                plot_input_data(data_path,file_name,plots_folder,format_type = format_type,normalized=True)
                ## Plot PDs
                plot_PDs(output_path,M_max,normalized=True)
                ## Plot barcodes
                plot_barcodes(output_path,M_max,normalized=True)
            else:
                ## Plot input data
                plot_input_data(data_path,file_name,output_path,format_type = format_type,normalized=False)
                ## Plot PDs
                plot_PDs(output_path,M_max,normalized=False)
                ## Plot barcodes
                plot_barcodes(output_path,M_max,normalized=False)
        #-----------------------------------------------------------
    else:
        im = os.getcwd() 
        file_names = [] ## contains all desired files to compute PH (without extension)
        list_files = []
        for f in os.listdir(im):
            if f.endswith('.%s'%format_type):
                list_files.append(f) ## add to summary
                file_names.append(f.split('.%s'%format_type)[0])

        ## Plots ## 
        if(plots_on):
            ## check or create folder for plots
            plots_folder = '%s/plots'%output_path
            if not os.path.exists(plots_folder):
                os.makedirs(plots_folder)

        for file_name in list_files:
            ## Check input and read it
            M_max, M_shape = check_format_input(data_path,file_name,format_type=format_type)
            ## Execfile Ripser (for dim 0,1,2)
            exec_ripser(data_path,ripser_path,output_path, input_file='input.txt')
            ## read output ripser and convert to a nicer output
            output_name = file_name.split('.%s'%format_type)[0] ## name file withou extension
            read_ripser_output(output_path,output_name=output_name)
            ## create a summary of your data and results
            summary_output(output_path,M_shape,M_max,output_name=output_name)
            #-----------------------------------------------------------
            ## Plots ## 
            if(plots_on):
                if(normalized):
                    ## Plot input data
                    plot_input_data(data_path,file_name,plots_folder,format_type = format_type,normalized=True,output_name=output_name)
                    ## Plot PDs
                    plot_PDs(output_path,M_max,normalized=True,output_name=output_name)
                    ## Plot barcodes
                    plot_barcodes(output_path,M_max,normalized=True,output_name=output_name)
                else:
                    ## Plot input data
                    plot_input_data(data_path,file_name,output_path,format_type = format_type,normalized=False,output_name=output_name)
                    ## Plot PDs
                    plot_PDs(output_path,M_max,normalized=False,output_name=output_name)
                    ## Plot barcodes
                    plot_barcodes(output_path,M_max,normalized=False,output_name=output_name)
            #-----------------------------------------------------------
    return()

## parameters 
ripser_path = '/home/%s/Software/ripser'%computer
data_path = '/home/%s/Dropbox/ISI_Esther/Easy_PH/tmp'%computer
output_path = '/home/%s/Dropbox/ISI_Esther/Easy_PH/tmp'%computer
file_name = 'test1.txt'

main_function(data_path,'txt',output_path=None,plots_on=False)
main_function(data_path,'txt',file_name = file_name,output_path=None,plots_on=False)
main_function(data_path,'txt',file_name = file_name,output_path=None,plots_on=True)
main_function(data_path,'txt',output_path=None,plots_on=True)

# -----------------------------


# ----------------------------
## main ##
# -----------------------------
## Check input and read it
M_max, M_shape = check_format_input(data_path,file_name,format_type='txt')
## Execfile Ripser (for dim 0,1,2)
exec_ripser(data_path,ripser_path,input_file='input.txt')
## read output ripser and convert to a nicer output
read_ripser_output(output_path)
## create a summary of your data and results
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

