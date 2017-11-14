### Plot functions ###
import pickle as pk
import networkx as nx
import numpy as np
import pylab as plt
import pandas as pd
import seaborn as sns

## Figure heatmat input data
def plot_input_data(data_path,file_name,output_path,normalized=False):
    M_max, M = check_format_input(data_path,file_name,format_type='txt',return_M = True)
    plt.figure()
    plt.subplot(111,aspect='equal')
    if(normalized):
        plt.imshow(M/float(M_max), cmap=plt.cm.Oranges, interpolation="nearest")
        plt.colorbar(vmin=0,vmax=1)
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
def plot_PDs(output_path,M_max,normalized=False,norm_by =None):
    """
    normalized= True or False
    norm_by = max_M or  max_bydim 
    """
    data = pd.read_csv(output_path+'/outputs_PDS.csv',index_col = 0)
    plt.figure(figsize=(15,5))
    if(normalized):
        if(norm_by!=None):
            if(norm_by == 'max_M'):
                for i in range(1,4):
                    plt.subplot(1,3,i, aspect='equal')
                    plt.plot(data[data.dimH==i-1].birth.values/np.float(M_max),data[data.dimH==i-1].death.values/np.float(M_max),'bo',alpha=.3,label='dim %i'%(i-1))
                    plt.xlim((0,1)); plt.ylim((0,1))
                    frame = plt.legend(loc=4,frameon=True,title='norm max by max value')
                    frame = frame.get_frame()
                    frame.set_edgecolor('black')
                    plt.xlabel('birth'); plt.ylabel('death')
                    plt.plot([0, 1], [0, 1], ls="--", c=".3")
                plt.suptitle('Persistence Diagrams')
                plt.savefig('%s/PDs_norm_maxM.png'%output_path)
                print 'Saved PDs plots in %s/PDs_norm_maxM.png'%output_path
        else:#(norm_by == 'max_bydim'):
            for i in range(1,4):
                plt.subplot(1,3,i, aspect='equal')
                m_max = np.max(data[data.dimH==i-1].death.values)
                plt.plot(data[data.dimH==i-1].birth.values/np.float(m_max),data[data.dimH==i-1].death.values/np.float(m_max),'bo',alpha=.3,label='dim %i'%(i-1))
                plt.xlim((0,1)); plt.ylim((0,1))
                frame = plt.legend(loc=4,frameon=True,title='norm max by dim')
                frame = frame.get_frame()
                frame.set_edgecolor('black')
                plt.xlabel('birth'); plt.ylabel('death')
                plt.plot([0, 1], [0, 1], ls="--", c=".3")
            plt.suptitle('Persistence Diagrams')
            plt.savefig('%s/PDs_norm_max_bydim.png'%output_path)
            print 'Saved PDs plots in %s/PDs_norm_maxbydim.png'%output_path
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
def plot_barcodes(output_path,M_max,normalized=True,norm_by ='max_bydim'):
    """
    given output_path plot barcodes for dim 0,1,2
    normalized= True (plot lenghts bars normalized by 1) otherwise real weights
    norm_by ='max_M' or  'max_bydim'
    """
    data = pd.read_csv(output_path+'/outputs_PDS.csv',index_col = 0)
    plt.figure(figsize=(15,5))
    for j in range(1,4):
        plt.subplot(1,3,j)
        m_max = np.max(data[data.dimH==j-1].death.values)
        L = len(data[data.dimH==j-1].death.values)
        factor=np.sqrt(L);
        for i,pair in enumerate(zip(data[data.dimH==j-1].birth.values,data[data.dimH==j-1].death.values)):
            if(normalized and norm_by == 'max_M'):
                plt.plot([float(pair[0])/float(M_max),float(pair[1])/float(M_max)],[factor*(L-i), factor*(L-i)],'o-');
            elif(normalized and norm_by == 'max_bydim'):
                plt.plot([float(pair[0])/float(m_max),float(pair[1])/float(m_max)],[factor*(L-i), factor*(L-i)],'o-');
            else:
                plt.plot([float(pair[0]),float(pair[1])],[factor*(L-i), factor*(L-i)],'o-');
        plt.yticks([])
        if(normalized and norm_by == 'max_M'):
            plt.xlim((0,1))
            plt.xlabel('Normalized persistence by max value')
            plt.legend([],loc=1,title='dim %i'%(j-1))
            plt.suptitle('Barcodes')
            plt.savefig('%s/barcodes_norm_maxM.png'%output_path)
            print 'Saved barcodes plots in %s/barcodes_norm_maxM.png'%output_path
        elif(normalized and norm_by == 'max_bydim'):
            plt.xlim((0,1))
            plt.xlabel('Normalized persistence by max by dim')
            plt.legend([],loc=1,title='dim %i'%(j-1))
            plt.suptitle('Barcodes')
            plt.savefig('%s/barcodes_norm_maxbydim.png'%output_path)
            print 'Saved barcodes plots in %s/barcodes_norm_maxbydim.png'%output_path  
        else:
            plt.xlim((0,M_max))
            plt.xlabel('persistence')
            plt.legend([],loc=1,title='dim %i'%(j-1))
            plt.suptitle('Barcodes')
            plt.savefig('%s/barcodes.png'%output_path)
            print 'Saved barcodes plots in %s/barcodes.png'%output_path
    return()
