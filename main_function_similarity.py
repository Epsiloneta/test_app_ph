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


data_path = '%s/Dropbox/ISI_Esther/Easy_PH/tmp/results/'%userhome
data_path = '%s/Dropbox/ISI_Esther/paolo_moretti_networks/generated_networks/results/'%userhome
format_type = 'csv'
dim=1
normalized = True
dim = 1
plots_on =True
sim_weighted = False # todo if true
output_path = None
sigma = None

# \todo pass max_val_one as input (OPTIONAL)
def plots_similarity_matrix(sigma_range,sigma_2keep, sim_matrix_list,mean_sim,std_sim,plots_folder,max_val_one=True):
    """
    m: similarity matrix (full upper triangular matrix)
    """
    if(max_val_one):
        vmax=1
    else: 
        vmax = np.max([np.max(m) for m in sim_matrix_list])
    plt.figure(figsize=(12,17))
    if(len(sigma_range)==1):
        size = sim_matrix_list[0].shape[0]
        plt.imshow(sim_matrix_list[0],interpolation='None',vmin=0,vmax=vmax)
        plt.colorbar()
        plt.title('Similarity matrix: sigma %.3f \n mean similarity: %.3f, std similarity: %.3f'%(sigma_range[0],mean_sim[0],std_sim[0]))
    else:
        num_plots = len(sigma_2keep)
        size = sim_matrix_list[0].shape[0]
        for i,sigmai in zip(range(1,num_plots+1),sigma_2keep):
            plt.subplot(2,2,i)
            plt.imshow(sim_matrix_list[i-1],interpolation='None',vmin=0,vmax=vmax)
            plt.title('sigma %.3f, mean sim: %.3f, std sim: %.3f'%(sigmai,mean_sim[i-1],std_sim[i-1]))
        plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
        cax = plt.axes([0.85, 0.1, 0.075, 0.8])
        plt.colorbar(cax=cax)
        plt.suptitle('Similarity matrices')

    plot_file_name = os.path.join(plots_folder,'similarity_matrix.png')
    plt.savefig(plot_file_name)  
    # plt.show()
    return()


def plot_similarity_curve(sigma_range,mean_sim,std_sim,len_sample,plots_folder):
    """
    plot similarity curve ci of mean similarity in the group (ci at 95%)
    """

    plt.figure(figsize=(8,6))
    plt.xlabel('sigma',fontsize=20)
    plt.ylabel('Similarity', fontsize=25)
    plt.title('Group Similarity of Persistence Diagrams \nConfidence interval of mean similarity', fontsize=20)
    er = 1.96*std_sim/np.sqrt(len_sample)
    errorfill(np.array(sigma_range), mean_sim, er,color='b')
    plot_file_name = os.path.join(plots_folder,'similarity_curve.png')
    plt.savefig(plot_file_name)  
    # plt.show()
    return()

def errorfill(x, y, yerr, color=None, alpha_fill=0.3, ax=None,label=[]):
    """
    use:
        errorfill(x, y_sin, yerr)
    """
    ax = ax if ax is not None else plt.gca()
    # if color is None:
    #     # color = ax._get_lines.color_cycle.next() # old
    #     color = ax._get_lines.prop_cycler.next()
    if np.isscalar(yerr) or len(yerr) == len(y):
        ymin = y - yerr
        ymax = y + yerr
    elif len(yerr) == 2:
        ymin, ymax = yerr
    ## scaled
    ax.plot(x, y ,'o-',color=color,label=label)
    ax.fill_between(x, ymax, ymin, color=color, alpha=alpha_fill)
    ### unscaled
    # ax.plot(range(len(x)),y ,'o-',color=color,label=label)
    # ax.fill_between(range(len(x)),ymax, ymin, color=color, alpha=alpha_fill)
    # plt.xticks(range(len(x)), sigma_range)
    return()

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
        ind = [0]
    elif(type(sigma) == int or type(sigma) == float):
        sigma_range = [sigma]
        sigma_2keep = set(np.array(sigma_range))
        ind = [0]
    else:
        sigma_range = list(sigma) ## range of sigmas
        if(len(sigma_range)<4):
            ind = range(len(sigma_range))
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
            a = sim_matrix[np.triu_indices_from(sim_matrix,k=1)]
            mean_sim[index_sigma] = np.mean(a)
            std_sim[index_sigma] = np.std(a)
            print 'mean_sim ', mean_sim
            print 'std_sim ', std_sim
            len_sample = len(a)
            print 'len sample ', len_sample
    output_file_path = os.path.join(output_path,'similarity.csv')
    df_sim.to_csv(output_file_path) ## save pandas file with PDs for dim 0,1,2
    ## Plots ## 
    if(plots_on): 
        print 'sigma_range ', sigma_range
        print 'sigma_2keep ', sigma_2keep
        print 'sim_matrix_list ',sim_matrix_list
        print 'ind ', ind
        print 'mean sim ',mean_sim
        print 'std_sim ',std_sim

        print mean_sim[ind],std_sim[ind]
        plots_similarity_matrix(sigma_range,sigma_2keep, sim_matrix_list,mean_sim[ind],std_sim[ind],plots_folder)
        if(len(sigma_range)>1):
            plot_similarity_curve(sigma_range,mean_sim,std_sim,len_sample,plots_folder)
    return()




# sim_matrix_list  = [np.array([[  0.00000000e+00,   2.90358844e-04,   6.36422256e-03,
#           9.91411860e-03],
#        [  0.00000000e+00,   0.00000000e+00,   4.00827475e-02,
#           4.57490237e-04],
#        [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
#           7.80413372e-05],
#        [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00,
#           0.00000000e+00]]), np.array([[ 0.        ,  0.00769843,  0.01367194,  0.04855401],
#        [ 0.        ,  0.        ,  0.43573999,  0.00730463],
#        [ 0.        ,  0.        ,  0.        ,  0.00325588],
#        [ 0.        ,  0.        ,  0.        ,  0.        ]]), np.array([[ 0.        ,  0.01981697,  0.02192398,  0.14980117],
#        [ 0.        ,  0.        ,  0.7195568 ,  0.01705059],
#        [ 0.        ,  0.        ,  0.        ,  0.01169548],
#        [ 0.        ,  0.        ,  0.        ,  0.        ]]), np.array([[ 0.        ,  0.02334648,  0.02453401,  0.19059972],
#        [ 0.        ,  0.        ,  0.76619033,  0.01974415],
#        [ 0.        ,  0.        ,  0.        ,  0.01442011],
#        [ 0.        ,  0.        ,  0.        ,  0.        ]])]

# vmax = np.max([np.max(m) for m in sim_matrix_list])

# plt.figure(figsize=(12,17))
# num_plots = 4
# size = sim_matrix_list[0].shape[0]
# for i in range(1,num_plots+1):
#     ax = plt.subplot(2,2,i)
#     plt.imshow(sim_matrix_list[i-1],interpolation='None',vmin=0,vmax=vmax,cmap='Blues')
#     # plt.imshow(sim_matrix_list[i-1],interpolation='None',vmin=0,vmax=vmax)
#     plt.yticks([])
#     ax.plot([-0.5,3.5],[-0.5,3.5],'k')
#     plt.title('sigma 00000000000000 mean sim: , std sim: ')
# plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
# # plt.subplots_adjust(bottom=0.1, right=0., top=0.9)
# cax = plt.axes([0.85, 0.1, 0.075, 0.8])
# plt.colorbar(cax=cax)
# plt.suptitle('dgdgdhdhd')
# plt.show()

# \TODO similarity weighted
sigma=[0.1,0.3,0.6,0.7]
main_function(data_path,format_type,output_path=None,sim_weighted=False,sigma=sigma,plots_on=True,normalized=normalized,dim=dim)
# m = main_function(data_path,format_type,output_path=None,sim_weighted=False,sigma=[0.3,0.6],plots_on=True,normalized=normalized,dim=dim)
# a = np.triu_indices_from(m,k=1) ## triangular superior
# plt.imshow(m,interpolation='None')
# plt.title('Similarity matrix: sigma %.3f, %s')
# np.mean(a)
# np.std(a)
