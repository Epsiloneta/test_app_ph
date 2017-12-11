import Tkinter as tk
import tkFileDialog
import tkMessageBox
import os
# from tkFileDialog import askopenfilename

import re
from function_main import main_test, check_and_prepare_variables, main_function
from help_dialogs import info_inputs, info_maxdimension, info_formats, info_results, info_threshold
from menus_info import about_homology, about_persistent_homology_interpret, help_run_program, help_report_bugs_comments

# def donothing():
#    filewin = tk.Toplevel(root)
#    button = tk.Button(filewin, text="Do nothing button")
#    button.pack()

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.initUI()
        self.createMenu()



    def initUI(self):      
        self.master.title("Easy Persistent Homology")
        self.grid(row=0,column=0,columnspan=7,rowspan=8) 
        # self.create_menubar()
        self.createWidgets()
        self.createWidgets_optional()

    def browse_file_folder(self,var,b_type='folder',normalize=False):
        if b_type is 'folder':
            filename = tkFileDialog.askdirectory()
        if b_type is 'file':
            filename = tkFileDialog.askopenfilename()

        if normalize:
            filename = os.path.basename(filename)

        var.set(filename)

    def createMenu(self):
        self.menubar = tk.Menu(self)

        self.aboutmenu = tk.Menu(self.menubar, tearoff=0)
        self.aboutmenu.add_command(label="Homology and Persistent Homology", command=about_homology)
        self.aboutmenu.add_command(label="Persistent Homology interpretation", command=about_persistent_homology_interpret)
        
        self.menubar.add_cascade(label="About", menu=self.aboutmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Run Easy Persistent Homology", command=help_run_program)
        self.helpmenu.add_command(label="Report bugs and comments", command=help_report_bugs_comments)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

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
        self.button_data_path = tk.Button(self,text="Folder data", 
            command=lambda: self.browse_file_folder(self.folder_path_input),
            font='Verdana 12 bold')
        self.button_data_path.grid(row=0, column=1,sticky=tk.W+tk.E)

        ###################################################################
        ## select format files
        self.lab_format_files = tk.Label(self,text="Input file/s format",
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
        self.execute_button = tk.Button(self,command=self.safe_launch_computation,font='Verdana 12 bold')
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
        self.button_file_path = tk.Button(self,text="File to analyse", 
            command=lambda :self.browse_file_folder(self.file_path_input,b_type='file',normalize=True))
        self.button_file_path.grid(row=0, column=3)

        ## ----------------------------------------------------------
        ## output data path
        # \todo add output folder as optional and data folder as default
        # \todo add input folder starting path from: on sigui
        self.folder_path_output = tk.StringVar()
        self.label_folder2 = tk.Label(self,textvariable=self.folder_path_output,width=40,height=2)
        self.label_folder2.grid(row=1, column=5)
        self.button_output_path = tk.Button(self,text="Output folder", 
            command=lambda: self.browse_file_folder(self.folder_path_output)
            )
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
        self.dim_max0 = tk.Radiobutton(self, text="0 (connected components)", variable=self.var_dim, value=0)
        self.dim_max0.grid(row=3, column=1,sticky=tk.W)
        self.dim_max1 = tk.Radiobutton(self, text="1 (cycles)", variable=self.var_dim, value=1)
        self.dim_max1.grid(row=4, column=1,sticky=tk.W)
        self.dim_max2 = tk.Radiobutton(self, text="2 (voids)", variable=self.var_dim, value=2)
        self.dim_max2.grid(row=5, column=1,sticky=tk.W)
        ##################################################################
        ## optional features (threshold - focused on inputs coming from unweighted networks where we have added weight to non existent edges to avoid distance 0)
        self.label_opt_features = tk.Label(self, text="Optional Features:")
        self.label_opt_features.grid(row=6, column=1,sticky=tk.W)
        ## info button 
        self.info_opt_feature_th = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=info_threshold)
        self.info_opt_feature_th.grid(row=6,column = 0,sticky=tk.W)

        self.optional_th = tk.Label(self, text="Threshold:")
        self.optional_th.grid(row=7, column=1,sticky=tk.W)
        self.entry_th = tk.Entry(self)
        self.entry_th.grid(row=8, column=1,sticky=tk.W)


    def launch_computation(self):
        print 'launching...'

        data_path=self.folder_path_input.get()

        print 'data path ',data_path
        format_type,lower_matrix,upper_matrix,file_name,output_path,file_name, threshold = check_and_prepare_variables(
            self.folder_path_input.get(),
            self.var_format.get(),
            self.file_path_input.get(),
            self.folder_path_output.get(),
            self.entry_th.get()
            )
        
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
            max_dim=self.var_dim.get(),
            threshold = threshold
            )

        print 'launching Easy PH... '

        main_function(data_path,format_type,file_name=file_name,lower_matrix = lower_matrix, upper_matrix = upper_matrix, 
            output_path=output_path,plots_on=plots_on,normalized=normalized,max_dim=max_dim,threshold=threshold)
        if(output_path==None):
            print 'Go to check your results at %s/results!'%self.folder_path_input.get()
        else:
            print 'Go to check your results at %s/results!'%output_path


    def safe_launch_computation(self):
        try:
            self.launch_computation()
        except Exception as e:
            s = str(e)
            raise(e)
            tkMessageBox.showerror("Error",s)
        


# main_function(data_path,format_type,file_name=None,lower_matrix = False, upper_matrix = False, output_path=None,plots_on=True,normalized=False,max_dim=1):
    
# \todo error fer q surti pantalleta 
def run_app():
    root = tk.Tk()
    root.grid_columnconfigure(7, minsize=100) 
    app = Application(master=root)
    app.mainloop()

if __name__=='__main__':
    run_app()
