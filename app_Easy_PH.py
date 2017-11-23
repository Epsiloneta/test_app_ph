import Tkinter as tk
import tkFileDialog
import os
# from tkFileDialog import askopenfilename

import re
from function_main import main_test, check_and_prepare_variables, main_function
from help_dialogs import info_inputs, info_maxdimension, info_formats, info_results

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.initUI()

    def initUI(self):
      
        self.master.title("Easy Persistent Homology")
        # self.pack(fill=tk.BOTH, expand=1)
        # self.pack()
        self.grid(row=0,column=0,columnspan=7,rowspan=8)  
        self.createWidgets()
        self.createWidgets_optional()

    def browse_button_input(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        # global folder_path_input
        filename = tkFileDialog.askdirectory()
        self.folder_path_input.set(filename)
        print(filename)

    def browse_button_output(self):
        # Allow user to select a directory and store it in global var
        # called folder_path
        # global folder_path_output
        filename = tkFileDialog.askdirectory()
        self.folder_path_output.set(filename)
        print(filename)
    
    def browse_button_file(self):
        # Allow user to select a directory and store it in global var
        filename = tkFileDialog.askopenfilename()
        filename = os.path.basename(filename)
        self.file_path_input.set(filename)
        print(filename)

    def createWidgets(self):
        ###################################################################
        ## select folder data
        ## info button 
        self.info_input = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_inputs)
        self.info_input.grid(row=0,column = 0,sticky=tk.W)
        self.folder_path_input = tk.StringVar()
        self.label_folder1 = tk.Label(self,textvariable=self.folder_path_input,width=40,height=2)
        self.label_folder1.grid(row=1, column=1)
        self.button_data_path = tk.Button(self,text="Folder data", command=self.browse_button_input,font='Verdana 12 bold')
        self.button_data_path.grid(row=0, column=1,sticky=tk.W+tk.E)

        ###################################################################
        ## select format files
        self.lab_format_files = tk.Label(self,text="Format input file/s",
            font = "Verdana 12 bold") #  fg = "blue",bg = "white",
        self.lab_format_files.grid(row=2, column=3,sticky=tk.W)
        self.var_format = tk.StringVar(None,"txt")
        ## info button 
        self.info_format = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_formats)
        self.info_format.grid(row=2,column = 2,sticky=tk.W)
        self.format1 = tk.Radiobutton(self, text="txt", variable=self.var_format, value='txt')
        self.format1.grid(row=3, column=3,sticky=tk.W)
        self.format2 = tk.Radiobutton(self, text="csv", variable=self.var_format, value='csv')
        self.format2.grid(row=4, column=3,sticky=tk.W)
        self.format3 = tk.Radiobutton(self, text="npy", variable=self.var_format, value='npy')
        self.format3.grid(row=5, column=3,sticky=tk.W)
        self.format4 = tk.Radiobutton(self, text="gpickle", variable=self.var_format, value='gpickle')
        self.format4.grid(row=6, column=3,sticky=tk.W)
        self.format5 = tk.Radiobutton(self, text="txt (lower dist-matrix)", variable=self.var_format, value='txt-lowdist')
        self.format5.grid(row=7, column=3,sticky=tk.W)
        self.format6 = tk.Radiobutton(self, text="txt (upper dist-matrix)", variable=self.var_format, value='txt-updist')
        self.format6.grid(row=8, column=3,sticky=tk.W)
        ##################################################################
        ## Execute programm button ##
        self.execute_button = tk.Button(self,command=self.launch_computation,font='Verdana 12 bold')
        self.execute_button["text"] = "Run program"
        self.execute_button["fg"]   = "blue"
        self.execute_button.grid(row=0, column=6)
        ## ----------------------------------------------------------

    def createWidgets_optional(self):
        ## label results 
        self.lab_results = tk.Label(self,text="Results",
            font = "Verdana 12 bold") # fg = "blue",bg = "white",
        self.lab_results.grid(row=2, column=5,sticky=tk.W)
        ## info button 
        self.info_results1 = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_results)
        self.info_results1.grid(row=2,column = 4,sticky=tk.W)
        ## ------------- OPTIONAL ----------------------------------
        ## select specific file to analyse
        # # self.data_file = tk.askopenfilename(initialdir = "C:/<whatever>")
        self.file_path_input = tk.StringVar()
        self.label_folder3 = tk.Label(self,textvariable=self.file_path_input,width=30,height=2)
        self.label_folder3.grid(row=1, column=3)
        self.button_file_path = tk.Button(self,text="File to analyse", command=self.browse_button_file)
        self.button_file_path.grid(row=0, column=3)

        ## ----------------------------------------------------------
        ## output data path
        # \todo add output folder as optional and data folder as default
        # \todo add input folder starting path from: on sigui
        self.folder_path_output = tk.StringVar()
        self.label_folder2 = tk.Label(self,textvariable=self.folder_path_output,width=40,height=2)
        self.label_folder2.grid(row=1, column=5)
        self.button_output_path = tk.Button(self,text="Output folder", command=self.browse_button_output)
        self.button_output_path.grid(row=0, column=5,sticky=tk.W)

        ## ----------------------------------------------------------
        ## generate plots
        self.plots_on = tk.BooleanVar()
        self.plots_on.set(True)
        self.plots = tk.Checkbutton(self,text ='Generate Plots',variable = self.plots_on)
        self.plots.grid(row=3, column=5,sticky=tk.W)
        ## ----------------------------------------------------------
        ## plots normalized
        self.plots_norm = tk.BooleanVar()
        self.plots_norm.set(False)
        self.plots_n = tk.Checkbutton(self,text ='Normalized plots',variable = self.plots_norm)
        self.plots_n.grid(row=4, column=5,sticky=tk.W)
        ###################################################################
        # max dimension to compute persistent homology
        ## info button 
        self.info_dim = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_maxdimension)
        self.info_dim.grid(row=2,column = 0,sticky=tk.W)
        self.lab_dim_max = tk.Label(self,text="Max dimension to compute\n persistent homology",
            font = "Verdana 12 bold") # fg = "blue",bg = "white",
        self.lab_dim_max.grid(row=2, column=1,sticky=tk.W)
        self.var_dim = tk.IntVar(None,1)
        self.dim_max0 = tk.Radiobutton(self, text="0", variable=self.var_dim, value=0)
        self.dim_max0.grid(row=3, column=1,sticky=tk.W)
        self.dim_max1 = tk.Radiobutton(self, text="1", variable=self.var_dim, value=1)
        self.dim_max1.grid(row=4, column=1,sticky=tk.W)
        self.dim_max2 = tk.Radiobutton(self, text="2", variable=self.var_dim, value=2)
        self.dim_max2.grid(row=5, column=1,sticky=tk.W)
        ##################################################################


    def launch_computation(self):
        print 'launching...'

        data_path=self.folder_path_input.get()
        format_type,lower_matrix,upper_matrix,file_name,output_path,file_name = check_and_prepare_variables(
            self.folder_path_input.get(),self.var_format.get(),
            self.file_path_input.get(),
            self.folder_path_output.get())

        plots_on=self.plots_on.get()
        normalized=self.plots_norm.get()
        max_dim=self.var_dim.get()

        print 'Your input variables are the following:'
        main_test(data_path=self.folder_path_input.get(),
            format_type=format_type,
            file_name = file_name,
            lower_matrix = lower_matrix,
            upper_matrix = upper_matrix,
            output_path = output_path,
            plots_on=self.plots_on.get(),
            normalized=self.plots_norm.get(),
            max_dim=self.var_dim.get())

        print 'launching Easy PH... '

        main_function(data_path,format_type,file_name=file_name,lower_matrix = lower_matrix, upper_matrix = upper_matrix, 
            output_path=output_path,plots_on=plots_on,normalized=normalized,max_dim=max_dim)

        if(output_path==None):
            print 'Go to check your results at %s/results!'%self.folder_path_input.get()
        else:
            print 'Go to check your results at %s/results!'%output_path
        



# main_function(data_path,format_type,file_name=None,lower_matrix = False, upper_matrix = False, output_path=None,plots_on=True,normalized=False,max_dim=1):
    
# \todo error fer q surti pantalleta 


root = tk.Tk()
root.grid_columnconfigure(7, minsize=100) 
app = Application(master=root)
app.mainloop()

# root.quit()