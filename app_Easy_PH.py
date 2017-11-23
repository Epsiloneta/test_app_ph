import Tkinter as tk
import tkFileDialog
# from tkFileDialog import askopenfilename

import re
from function_main import main_test, check_and_prepare_variables, main_function

class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def HighlightPattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")





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
        # filename = tkFileDialog.askopenfilename(initialdir = self.folder_path_input+"/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        filename = filename.split('/')[-1]
        self.file_path_input.set(filename)
        print(filename)

    def createWidgets(self):
        ###################################################################
        ## select folder data
        ## info button 
        self.info_input = tk.Button(self,text ="info", relief=tk.RAISED,\
                         bitmap="info",command=self.info_inputs)
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
                         bitmap="info",command=self.info_formats)
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
                         bitmap="info",command=self.info_results)
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
                         bitmap="info",command=self.info_maxdimension)
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
    

    def info_inputs(self):
        win = tk.Toplevel()
        win.title("About Input / Output path")
        about = '''
        'Folder data' (compulsory): select folder where your data is saved. Compulsory field to run the program. Program analyse all files inside this folder with the given format file ('txt','csv','npy','gpickle').

        'File to analyse' (optional, empty by default): If you only want to analyse a file please select 'Folder data' as the folder where your file is and then select the file in the possible formats ('txt','csv','npy','gpickle'). Your file extension must be the same than the selected 'Format input file/s'

        'Output folder' (optional, if empty, it will be by default 'Folder data'): Folder path where you want to save output results from the program. 
        '''

        # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
        t=CustomText(win, wrap="word", width=100, height=15, borderwidth=0)
        t.tag_configure("blue", foreground="blue")
        t.pack(sid="top",fill="both",expand=True)
        t.insert("1.0", about)
        t.HighlightPattern("Folder data", "blue")
        t.HighlightPattern("File to analyse", "blue")
        t.HighlightPattern("Output folder", "blue")
        t.HighlightPattern("optional", "blue")
        t.HighlightPattern("compulsory", "blue")
        tk.Button(win, text='OK', command=win.destroy).pack()


    def info_maxdimension(self):
        win = tk.Toplevel()
        win.title("About Maximum dimension to compute Persistent Homology")
        about = '''
              Homology counts the n-dimensional holes in a given space. The number of holes (how many) given a dimension is called: betti numbers. 
              Persistent Homology (PH) counts the evolution of n-dimensional holes in a given space.
              'n' refers to the dimension of the hole:

              0-dimensional holes: represent connected components
              1-dimensional holes: represent cycles
              2-dimensional holes: represent voids
              n-dimensional holes: represent cavities of n-dimension

              For example a torus has:

              number of 0-dimensional holes: 1
              number of 1-dimensional holes: 2
              number of 2-dimensional holes: 1
              number of n-dimensional holes with n>2: 0 (for all n>2)

              Options to choose (with interpretability):

              dim 0, dim 1 (default) and dim 2.

              If you choose dimension 0, holes will be computed only for dimension 0. 
              If you choose dimension 1, holes will be computed for dimension 0 and 1. 
              If you choose dimension 2, holes will be computed for dimension 0,1 and until 2. 
            '''
        # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
        t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
        t.tag_configure("blue", foreground="blue")
        t.pack(sid="top",fill="both",expand=True)
        t.insert("1.0", about)
        t.HighlightPattern("Homology", "blue")
        t.HighlightPattern("Persistent Homology", "blue")
        t.HighlightPattern("0-dimensional holes", "blue")
        t.HighlightPattern("1-dimensional holes", "blue")
        t.HighlightPattern("2-dimensional holes", "blue")
        tk.Button(win, text='OK', command=win.destroy).pack()

    def info_results(self):
        win = tk.Toplevel()
        win.title("About Results outputs and options")
        about = '''Results from the computation of Persistent Homology are the following:

              A folder called 'results' will be created in the output folder selection or as default inside the data folder. There you can find: 
              - summary.txt: contain a summary of the number of holes for each dimension and how many have persisted across a certain percentage of the total possible life.
              - outputs_PDS.csv: recap all holes for each dimension with its birth and death point.
              

              If you have actived the option Generate plots (True by default) another folder plots inside results will be created. There you will find persistent diagram plot and barcode plot (both plots shows the same results in different ways). Moreover if your input files are not lower/upper distance matrix (usually used if you are working with more than 10^4 shape size) also will be generated a representation of your input data.
              - barcodes.png
              - PDs.png
              - input_data.png


              Normalized plots (False by default): if active (True) all output plots will be normalized according the maximum value found in the input data.
                Example: "M" input distance matrix, max_M = max(M) then all values (v_i) in the plots will be converted to (v_i / max_M)
            '''

        # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
        t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
        t.tag_configure("blue", foreground="blue")
        t.pack(sid="top",fill="both",expand=True)
        t.insert("1.0", about)
        t.HighlightPattern("persistent diagram", "blue")
        t.HighlightPattern("barcode", "blue")
        t.HighlightPattern("Generate plots", "blue")
        t.HighlightPattern("Normalized plots", "blue")
        tk.Button(win, text='OK', command=win.destroy).pack()
    
    # \todo check if all values positive (info format)
    def info_formats(self):
        win = tk.Toplevel()
        win.title("About Format files")
        about = '''Files have to codify as a matrix the pairwaise relationship between objects. Input files are like distance matrices (obviously distance matrix are welcome). That is, higher value implies higer distance and viceversa. If you are using correlations you can convert your data using 1-correlation. Be carefull: All values have to be positive!!!

        Format files can have the following extensions:

              - 'txt': (by default) columns delimited by ',' and rows by newline
              - 'npy': commonly python array / matrix 
              - 'gpickle': commonly from networkx library in python

              Recommended format for big shape matrices (that greater then 10^4 points, matrix shape 10^4 x 10^4)
              - 'txt' (lower-dist matrix): lower matrix (without diagonal), columns delimited by ',' and rows by newline.
                Example:
                 1,             or  1
                 1,0,               1,0
                 3,0,1,             3,0,1
                 1,0,1,2,           1,0,1,2
            - 'txt' (upper-dist matrix): upper matrix (without diagonal), columns delimited by ',' and rows by newline.
                Example:
                 1,0,1,2,           1,0,1,2
                 3,0,1,             3,0,1
                 1,0,               1,0
                 1,             or  1

        If you select only a file to analyse format must coincide with the file extension.
        If you just select a Folder data, all your files in that folder with the selected extension will be analysed.
        '''

        # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
        t=CustomText(win, wrap="word", width=120, height=30, borderwidth=0)
        t.tag_configure("blue", foreground="blue")
        t.pack(sid="top",fill="both",expand=True)
        t.insert("1.0", about)
        t.HighlightPattern("Generate plots", "blue")
        t.HighlightPattern("big shape matrices", "blue")
        tk.Button(win, text='OK', command=win.destroy).pack()



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