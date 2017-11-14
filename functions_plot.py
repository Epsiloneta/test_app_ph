### Plot functions ###
import pickle as pk
import networkx as nx
import numpy as np
import pylab as plt
import pandas as pd
import seaborn as sns
from functions_PH import check_format_input
sns.set(style="darkgrid")


## Figure heatmat input data
def plot_input_data(data_path,file_name,output_path,format_type,normalized=False):
    """
    Plot input data (matrix)
    normalized = True or False (normalized by the maximum value of the input data)
    """
    M_max, M = check_format_input(data_path,file_name,format_type,return_M = True)
    plt.figure()
    plt.subplot(111,aspect='equal')
    if(normalized):
        plt.imshow(M/float(M_max), cmap=plt.cm.Oranges, interpolation="nearest")
        plt.colorbar()
        plt.title('Input data (normalized)')
        plt.savefig('%s/input_data_normalized.png'%output_path)
        print 'Saved input data plot in %s/input_data_normalized.png'%output_path
    else:
        plt.imshow(M, cmap=plt.cm.Oranges, interpolation="nearest")
        plt.colorbar()
        plt.title('Input data')
        plt.savefig('%s/input_data.png'%output_path)
        print 'Saved input data plot in %s/input_data.png'%output_path
    return()

## Figure PDs (density points) for dim 0, 1, 2 
def plot_PDs(output_path,M_max,normalized=False):
    """
    normalized= True or False (normalized by the maximum value of the input data)
    """
    data = pd.read_csv(output_path+'/outputs_PDS.csv',index_col = 0)
    plt.figure(figsize=(15,5))
    if(normalized):
        for i in range(1,4):
            plt.subplot(1,3,i, aspect='equal')
            plt.plot(data[data.dimH==i-1].birth.values/np.float(M_max),data[data.dimH==i-1].death.values/np.float(M_max),'bo',alpha=.3,label='dim %i'%(i-1))
            plt.xlim((0,1)); plt.ylim((0,1))
            frame = plt.legend(loc=4,frameon=True,title='normalized')
            frame = frame.get_frame()
            frame.set_edgecolor('black')
            plt.xlabel('birth'); plt.ylabel('death')
            plt.plot([0, 1], [0, 1], ls="--", c=".3")
        plt.suptitle('Persistence Diagrams')
        plt.savefig('%s/PDs_normalized.png'%output_path)
        print 'Saved PDs plots in %s/PDs_normalized.png'%output_path
    else:
        for i in range(1,4):
            plt.subplot(1,3,i, aspect='equal')
            plt.plot(data[data.dimH==i-1].birth.values,data[data.dimH==i-1].death.values,'bo',alpha=.3,label='dim %i'%(i-1))
            plt.xlim((0,M_max)); plt.ylim((0,M_max))
            frame = plt.legend(loc=4,frameon=True)
            frame = frame.get_frame()
            frame.set_edgecolor('black')
            plt.xlabel('birth'); plt.ylabel('death')
            plt.plot([0, M_max], [0, M_max], ls="--", c=".3")
        plt.suptitle('Persistence Diagrams')
        plt.savefig('%s/PDs.png'%output_path)
        print 'Saved PDs plots in %s/PDs.png'%output_path
    return()

## Figure Barcodes for dim 0, 1, 2
def plot_barcodes(output_path,M_max,normalized=False):
    """
    given output_path plot barcodes for dim 0,1,2
    normalized= True or False (normalized by the maximum value of the input data) applied to the lenghts of bars
    """
    data = pd.read_csv(output_path+'/outputs_PDS.csv',index_col = 0)
    plt.figure(figsize=(15,5))
    for j in range(1,4):
        plt.subplot(1,3,j)
        m_max = np.max(data[data.dimH==j-1].death.values)
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
            plt.savefig('%s/barcodes_normalized.png'%output_path)
            
        else:
            plt.xlim((0,M_max))
            plt.xlabel('persistence')
            plt.legend([],loc=1,title='dim %i'%(j-1))
            plt.suptitle('Barcodes')
            plt.savefig('%s/barcodes.png'%output_path)
    if(normalized):
        print 'Saved barcodes plots in %s/barcodes_normalized.png'%output_path
    else:
        print 'Saved barcodes plots in %s/barcodes.png'%output_path
    return()
