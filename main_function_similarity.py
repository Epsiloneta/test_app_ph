import sys
import os
import pickle as pk
import networkx as nx
import numpy as np
import pandas as pd
import scipy.io
import timeit

## file with PH functions
from functions_kernel_similarity import *
# ## file with plot functions
# from functions_plot import *

# \TODO solve to put this here
# \TODO adapt '\' for windows
##########################################################
userhome = os.path.expanduser('~')
ripser_path = os.path.join(userhome,'Software/ripser')
##########################################################
# def compute_similarity(file1,file2,sim_weighted=False,alpha=None,plots_on=True,normalized=False,dim=1):


#     return()


data_path = '/home/esther/Dropbox/ISI_Esther/Easy_PH/tmp/results/'
data_path = '/home/esther/Dropbox/ISI_Esther/paolo_moretti_networks/generated_networks/results/'
format_type = 'csv'
dim=1
normalized = True
dim = 1
plots_on =False
sim_weighted = False
output_path = None
sigma = None


def main_function(data_path,format_type,output_path=None,sim_weighted=False,sigma=None,plots_on=True,normalized=False,dim=1):
    """
    data_path: folder path where data is. It will be used as folder where there are all files to compute PH
        Example: '/home/esther/Dropbox/ISI_Esther/Easy_PH/tmp'
    format_type: format of files to analyse: 'txt','csv'
    
    OPTIONAL:
    output_path: path to save results, if None then output_path will be in data_path (by default: None)
    sim_weighted=False 'use weighted similarity'
    alpha = None (range(alpha) or float) similarity kernel parameter. If None we will use a range() \todo define range
    plots_on: True or False. Decide if you want to generate also plots of the results. Matrix of similarities
    normalized: use normalized kernel or not
    dim = 1(if your file comes from output Easy PH, you can select from which dimension do you want to compute similarity
    """
    ## create folder with results
    if(output_path == None): output_path = data_path
    output_path = os.path.join(output_path,'results_similarities')
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    list_files = []  ## contains all desired files to compute PH (without extension)
    for f in os.listdir(data_path):
        if f.endswith('.%s'%format_type):
            list_files.append(f) ## add to summary
    list_files = list_files[:10]
    print 'list_files to compute similarity measure',list_files
    number_files = len(list_files)
    ## Plots ## 
    if(plots_on):
        ## check or create folder for plots
        plots_folder = os.path.join(output_path,'plots_similarities')
        if not os.path.exists(plots_folder):
            os.makedirs(plots_folder)

    if sigma == None:
        sigma_range = [0.5]
        sigma_2keep = set(np.array(sigma_range))
    elif(type(sigma) == int or type(sigma) == float):
        sigma_range = [sigma]
        sigma_2keep = set(np.array(sigma_range))
    else:
        sigma_range = list(sigma) ## range of sigmas
        if(len(sigma_range)<4):
            sigma_2keep = set(np.array(sigma_range))
        else:
            ind = map(int,np.linspace(0,len(sigma_range)-1,4))
            sigma_2keep = set(np.array(sigma_range)[ind])


    ## save results
    df_sim = pd.DataFrame()
    ## save max 4 similarity matrix 
    sim_matrix_list = [0]*len(sigma_range)
    mean_sim = np.zeros(len(sigma_range))
    std_sim = np.zeros(len(sigma_range))
    ii_aux = 0 
    #############################################
    for index_sigma,sigma in enumerate(sigma_range):
        print 'sigma ', sigma
        if(normalized):
            print list_files
            ### prepare computation
            auto_dist = dict()
            create_auto_dist(auto_dist,data_path,list_files,weighted=False,sigma=sigma)

        ### compute similarity by pairs
        names1 = [0]*int(number_files*(number_files-1)/2.)
        names2 = [0]*int(number_files*(number_files-1)/2.)
        sigmas_list = np.zeros(int(number_files*(number_files-1)/2.))
        sim_list = np.zeros(int(number_files*(number_files-1)/2.))

        sim_matrix = np.zeros((number_files,number_files))
        ## file_name devi esssere complete path? if yes:base=os.path.basename('/root/dir/sub/file.ext')

        index = 0
        for i,file_name1 in enumerate(list_files,start=0):
            for j in range(i+1,number_files): 
                print 'ij', i,j
                file_name2 = list_files[j]
                name1 = os.path.splitext(file_name1)[0]
                name2 = os.path.splitext(file_name2)[0]
                names1[index] = name1
                names2[index] = name2

                complete_path1 = os.path.join(data_path,file_name1)
                complete_path2 = os.path.join(data_path,file_name2)

                df1 = read_PDs(complete_path1)
                df2 = read_PDs(complete_path2)
                F = points_PD(df1,dim=dim)
                G = points_PD(df2,dim=dim)
                ## Compute similarity
                if(normalized):
                    k = kernel_reininghaus_normalized(sigma,F,G,with_auto_dist=auto_dist[(name1,sigma)]+ auto_dist[(name2,sigma)] )
                else:
                    k = kernel_reininghaus(sigma,F,G)

                ## upgrade similarity matrix 
                sim_matrix[i,j] = k

                sim_list[index] = k
                sigmas_list[index] = sigma
                index = index +1
        aux_data = pd.DataFrame()
        aux_data['id1'] = names1
        aux_data['id2'] = names2
        aux_data['similarity'] = sim_list
        aux_data['sigma'] = sigmas_list
        df_sim = df_sim.append(aux_data,ignore_index=True)

        if(plots_on):
            if(sigma in sigma_2keep):
                sim_matrix_list[ii_aux] = sim_matrix
                ii_aux = ii_aux +1 ##we only save 4 matrix max

            ## to plot similarity curve 
            a = np.triu_indices_from(sim_matrix,k=1)
            mean_sim[index_sigma] = np.mean(a)
            std_sim[index_sigma] = np.std(a)

    output_file_path = os.path.join(output_path,'similarity.csv')
    df_sim.to_csv(output_file_path) ## save pandas file with PDs for dim 0,1,2
    ## Plots ## 
    if(plots_on):


        fig, (ax1, ax2) = plt.subplots(1,2)
        p1 = ax1.imshow(sim_matrix,interpolation = None,aspect='equal',cmap=plt.get_cmap('Reds'))
        plt.colorbar(p1,ax=ax1)
        p2 = ax2.imshow(sim_matrix/np.max(sim_matrix),interpolation = None,aspect='equal',cmap=plt.get_cmap('Reds'))
        plt.colorbar(p2,ax=ax2)
        plt.show()
    return(sim_matrix)


def plots_similarity_matrix(sigma_range,sigma_2keep, sim_matrix_list,mean_sim,std_sim):
    """
    m: similarity matrix (full upper triangular matrix)
    """
    if(len(sigma_range)==1):
        # m = main_function(data_path,format_type,output_path=None,sim_weighted=False,sigma=[0.3,0.6],plots_on=True,normalized=normalized,dim=dim)
        a = np.triu_indices_from(sim_matrix_list[0],k=1) ## triangular superior
        mean_sim = np.mean(a)
        std_sim = np.std(a)
        plt.imshow(sim_matrix_list[0],interpolation='None')
        plt.colorbar()
        plt.title('Similarity matrix: sigma %.3f \n mean similarity: %.3f, std similarity: %.3f'%(sigma_range[0],mean_sim,std_sim))
        plt.show()
    else:
        num_plots = len(sigma_2keep)
        for i,sigmai in zip(range(1,num_plots+1),sigma_2keep):
            plt.subplot(2,2,i)
            a = np.triu_indices_from(sim_matrix_list[i-1],k=1) ## triangular superior
            mean_sim = np.mean(a)
            std_sim = np.std(a)
            plt.imshow(sim_matrix_list[i-1], ,interpolation='None')
            plt.title('sigma %.3f \n mean sim: %.3f, std sim: %.3f'%(sigmai,list(mean_sim),std_sim))

        plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
        cax = plt.axes([0.85, 0.1, 0.075, 0.8])
        plt.colorbar(cax=cax)
        plt.suptitle('Similarity matrices')
        
        plt.show()





m = main_function(data_path,format_type,output_path=None,sim_weighted=False,sigma=[0.3,0.6],plots_on=True,normalized=normalized,dim=dim)
a = np.triu_indices_from(m,k=1) ## triangular superior
plt.imshow(m,interpolation='None')
plt.title('Similarity matrix: sigma %.3f, %s')
np.mean(a)
np.std(a)


# plt.subplot(211)
# plt.imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)
# plt.subplot(212)
# plt.imshow(np.random.random((100, 100)), cmap=plt.cm.BuPu_r)

# plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
# cax = plt.axes([0.85, 0.1, 0.075, 0.8])
# plt.colorbar(cax=cax)
# plt.show()

# fig, (ax1, ax2) = plt.subplots(1,2)
# p1 = ax1.imshow(sim_matrix,interpolation = None,aspect='equal',cmap=plt.get_cmap('Reds'))
# plt.colorbar(p1,ax=ax1)
# p2 = ax2.imshow(sim_matrix/np.max(sim_matrix),interpolation = None,aspect='equal',cmap=plt.get_cmap('Reds'))
# plt.colorbar(p2,ax=ax2)
# plt.show()