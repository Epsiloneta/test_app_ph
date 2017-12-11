
### Plot functions ###
import os 
import pickle as pk
import networkx as nx
import numpy as np
import matplotlib
matplotlib.use('agg')
import pylab as plt
import pandas as pd
import seaborn as sns
from functions_PH import check_format_input
sns.set(style="darkgrid")


## Figure heatmat input data
def plot_input_data(data_path,file_name,plots_folder,format_type,lower_matrix,upper_matrix,normalized=False,output_name=None):
    """
    Plot input data (matrix)
    data_path: where data is
        Example: '/home/esther/Dropbox/ISI_Esther/Easy_PH/'
    file_name: file with data to plot
        Example: 'test1.txt'
    plots_folder: path inside ouputpath where plots are saved
        Example: '/home/esther/Dropbox/ISI_Esther/Easy_PH/results/plots/''
    format_type: format of data files (txt,npy,gpickle,csv)
        Example: 'txt'
    lower_matrix and upper_matrix: boolean (True or False) in case that your data is given by a lower / upper matrix (without diagonal) in a txt format. Usally when your data is too big to open as a matrix and load all the matrix in the memory. Both values are by default False.
    normalized = True or False (normalized by the maximum value of the input data)
    output_name: if we are computing PH on a set of files the output names of the plots will be the name of the data file + identification of the plot.
    """
    if output_name is None:
        aux = ['input_data']
    else:
        aux = [output_name,'input_data']
    if normalized is True:
        aux.append('normalized')
    plot_file_name = '-'.join(aux)+'.png'
    plot_file_name = os.path.join(plots_folder,plot_file_name)

    M_max, M = check_format_input(data_path,file_name,lower_matrix,upper_matrix,format_type,return_M = True,create_input_file=False)
    plt.figure()
    plt.subplot(111,aspect='equal')
    if(normalized):
        plt.imshow(M/float(M_max), cmap=plt.cm.Oranges, interpolation="nearest")
        plt.colorbar()
        plt.title('Input data (normalized)')

        plt.savefig(plot_file_name)
        print 'Saved input data plot in %s' % plot_file_name
    else:
        plt.imshow(M, cmap=plt.cm.Oranges, interpolation="nearest")
        plt.colorbar()
        plt.title('Input data')
        plt.savefig(plot_file_name)
        print 'Saved input data plot in %s' % plot_file_name
    return()

## Figure PDs (density points) for dim 0, 1, 2 
def plot_PDs(output_path,M_max,max_dim,normalized=False,output_name=None):
    """
    normalized= True or False (normalized by the maximum value of the input data)
    """
    plots_folder = os.path.join(output_path,'plots')
    if output_name is None: 
        aux = ['PDs']
        input_file = os.path.join(output_path,'outputs_PDS.csv')
    else:
        aux = [output_name,'PDs']
        input_file = os.path.join(output_path,'%s_PDS.csv' % output_name)
    if normalized is True:
        aux.append('normalized')
    plot_file_name = '-'.join(aux)+'.png'
    plot_file_name = os.path.join(plots_folder,plot_file_name)

    
    data = pd.read_csv(input_file,index_col = 0)
    

    fig_size_aux = 15/(3-max_dim)
    plt.figure(figsize=(fig_size_aux,5))
    if(normalized):
        for i in range(1,max_dim+2):
            plt.subplot(1,max_dim+1,i, aspect='equal')
            plt.plot(data[data.dimH==i-1].birth.values/np.float(M_max),data[data.dimH==i-1].death.values/np.float(M_max),'bo',alpha=.3,label='dim %i'%(i-1))
            plt.xlim((0,1)); plt.ylim((0,1))
            frame = plt.legend(loc=4,frameon=True,title='normalized')
            frame = frame.get_frame()
            frame.set_edgecolor('black')
            plt.xlabel('birth'); plt.ylabel('death')
            plt.plot([0, 1], [0, 1], ls="--", c=".3")
        plt.suptitle('Persistence Diagrams')
        plt.savefig(plot_file_name)
        print 'Saved PDs plots in %s'%plot_file_name
    else:
        for i in range(1,max_dim+2):
            plt.subplot(1,max_dim+1,i, aspect='equal')
            plt.plot(data[data.dimH==i-1].birth.values,data[data.dimH==i-1].death.values,'bo',alpha=.3,label='dim %i'%(i-1))
            plt.xlim((0,M_max)); plt.ylim((0,M_max))
            frame = plt.legend(loc=4,frameon=True)
            frame = frame.get_frame()
            frame.set_edgecolor('black')
            plt.xlabel('birth'); plt.ylabel('death')
            plt.plot([0, M_max], [0, M_max], ls="--", c=".3")
        plt.suptitle('Persistence Diagrams')
        plt.savefig(plot_file_name)
        print 'Saved PDs plots in %s'%plot_file_name
    return()

## Figure Barcodes for dim 0, 1, 2
def plot_barcodes(output_path,M_max,max_dim,normalized=False,output_name=None):
    """
    given output_path plot barcodes for dim 0,1,2
    normalized= True or False (normalized by the maximum value of the input data) applied to the lenghts of bars
    """
    plots_folder = os.path.join(output_path,'plots')
    if output_name is None: 
        aux = ['barcodes']
        input_file = os.path.join(output_path,'outputs_PDS.csv')
    else:
        aux = [output_name,'barcodes']
        input_file = os.path.join(output_path,'%s_PDS.csv' % output_name)
    if normalized is True:
        aux.append('normalized')
    plot_file_name = '-'.join(aux)+'.png'
    plot_file_name = os.path.join(plots_folder,plot_file_name)

    data = pd.read_csv(input_file,index_col = 0) 

    fig_size_aux = 15/(3-max_dim)
    plt.figure(figsize=(fig_size_aux,5))
    for j in range(1,max_dim+2):
        plt.subplot(1,max_dim+1,j)
        L = len(data[data.dimH==j-1].death.values)
        factor=np.sqrt(L);
        for i,pair in enumerate(zip(data[data.dimH==j-1].birth.values,data[data.dimH==j-1].death.values)):
            if(normalized):
                plt.plot([float(pair[0])/float(M_max),float(pair[1])/float(M_max)],[factor*(L-i), factor*(L-i)],'o-');
            else:
                plt.plot([float(pair[0]),float(pair[1])],[factor*(L-i), factor*(L-i)],'o-');
        plt.yticks([])
        if(normalized):
            plt.xlim((0,1))
            plt.xlabel('Normalized persistences')
            plt.legend([],loc=1,title='dim %i'%(j-1))
            plt.suptitle('Barcodes')
            plt.savefig(plot_file_name)
            print 'Saved barcodes plot in %s'%plot_file_name
        else:
            plt.xlim((0,M_max))
            plt.xlabel('persistence')
            plt.legend([],loc=1,title='dim %i'%(j-1))
            plt.suptitle('Barcodes')
            plt.savefig(plot_file_name)
            print 'Saved barcodes plot in %s'%plot_file_name
    return()
