import Tkinter as tk
import tkFileDialog
# from tkFileDialog import askopenfilename

from function_main import main_test

# from Tkinter import Tk
# from tkFileDialog import askopenfilename

# # https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
# Tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)


# def browse_button(self, which="out"):
#     # Allow user to select a directory and store it in global var
#     # called folder_path
#     # global folder_path
#     filename = tkFileDialog.askdirectory()
#     if which == "in":
#         self.folder_path.set(filename)
#     elif which == "out":
#         self.folder_path2.set(filename)
#     print(filename)


# root = Tk()
# folder_path = StringVar()
# lbl1 = Label(master=root,textvariable=folder_path)
# lbl1.grid(row=0, column=1)
# button2 = Button(text="Browse", command=browse_button)
# button2.grid(row=0, column=3)


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.initUI()

    def initUI(self):
      
        self.master.title("Easy Persistent Homology")
        # self.pack(fill=tk.BOTH, expand=1)
        # self.pack()
        self.grid(row=0,column=0,columnspan=4,rowspan=8)
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
        self.file_path_input.set(filename)
        print(filename)

    def createWidgets(self):
        
        # ## si cliques s'obre askdirectory
        # self.data_path = tk.Button(self,command=browse_button)
        # self.data_path["text"] = "Folder data"
        # self.data_path["fg"]   = "black"
        # # self.data_path["command"] = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        # # self.data_path["command"] = tkFileDialog.askdirectory()
        # # self.data_path.pack({"side": "left"})
        # self.data_path.grid(row=0, column=0)
        ###################################################################
        ## new 
        self.folder_path_input = tk.StringVar()
        self.label_folder1 = tk.Label(self,textvariable=self.folder_path_input)
        self.label_folder1.grid(row=1, column=0)
        self.button_data_path = tk.Button(self,text="Folder data", command=self.browse_button_input)
        self.button_data_path.grid(row=0, column=0)

        ###################################################################
        ## select format files
        self.lab_format_files = tk.Label(self,text="Format input file/s",
            fg = "blue",bg = "white",font = "Verdana 12 bold") 
        self.lab_format_files.grid(row=2, column=1,sticky=tk.W)
        self.var_format = tk.StringVar(None,"txt")
        self.format1 = tk.Radiobutton(self, text="txt", variable=self.var_format, value='txt')
        self.format1.grid(row=3, column=1,sticky=tk.W)
        self.format2 = tk.Radiobutton(self, text="csv", variable=self.var_format, value='csv')
        self.format2.grid(row=4, column=1,sticky=tk.W)
        self.format3 = tk.Radiobutton(self, text="npy", variable=self.var_format, value='npy')
        self.format3.grid(row=5, column=1,sticky=tk.W)
        self.format4 = tk.Radiobutton(self, text="gpickle", variable=self.var_format, value='gpickle')
        self.format4.grid(row=6, column=1,sticky=tk.W)
        self.format5 = tk.Radiobutton(self, text="txt (lower dist-matrix)", variable=self.var_format, value='txt-lowdist')
        self.format5.grid(row=7, column=1,sticky=tk.W)
        self.format6 = tk.Radiobutton(self, text="txt (upper dist-matrix)", variable=self.var_format, value='txt-updist')
        self.format6.grid(row=8, column=1,sticky=tk.W)
        ##################################################################
        ## Execute programm button ##
        self.execute_button = tk.Button(self,command=self.launch_computation)
        self.execute_button["text"] = "Run programm"
        self.execute_button["fg"]   = "blue"
        # self.data_path.pack({"side": "left"})
        self.execute_button.grid(row=0, column=3)
        ## ----------------------------------------------------------

    def createWidgets_optional(self):
        ## label results 
        self.lab_results = tk.Label(self,text="Results",
            fg = "blue",bg = "white",font = "Verdana 10") 
        self.lab_results.grid(row=2, column=2)
        ## ------------- OPTIONAL ----------------------------------
        ## select specific file to analyse
        # ################################################################### old 
        # self.data_file = tk.Button(self)
        # self.data_file["text"] = "File to analyse"
        # self.data_file["fg"]   = "black"
        # # self.data_file["command"]=self.askopenfilename()
        # # self.data_file = tk.askopenfilename(initialdir = "C:/<whatever>")
        # # self.data_file["command"] =  self.askopenfilename()
        # self.data_file.grid(row=0, column=1)
        ################################################################### 
        ## new 
        self.file_path_input = tk.StringVar()
        self.label_folder3 = tk.Label(self,textvariable=self.file_path_input)
        self.label_folder3.grid(row=1, column=1)
        self.button_file_path = tk.Button(self,text="File to analyse", command=self.browse_button_file)
        self.button_file_path.grid(row=0, column=1)

        ## ----------------------------------------------------------
        ## output data path
        # ################################################################### old 
        # self.output_folder = tk.Button(self)
        # self.output_folder["text"] = "Output folder"
        # self.output_folder["fg"]   = "black"
        # # self.output_folder["command"] =  self.askopenfilename()
        # self.output_folder.grid(row=0, column=2)
        ###################################################################
        # new 
        # \todo add output folder as optional and data folder as default
        # \todo add input folder starting path from: on sigui
        self.folder_path_output = tk.StringVar()
        self.label_folder2 = tk.Label(self,textvariable=self.folder_path_output)
        self.label_folder2.grid(row=1, column=2)
        self.button_output_path = tk.Button(self,text="Output folder", command=self.browse_button_output)
        self.button_output_path.grid(row=0, column=2)



        ## ----------------------------------------------------------
        ## generate plots
        self.plots_on = tk.BooleanVar()
        self.plots_on.set(True)
        self.plots = tk.Checkbutton(self,text ='Generate Plots',variable = self.plots_on)
        self.plots.grid(row=3, column=2,sticky=tk.W)
        # self.plots
        # \todo ficar per defecte True
        # self.plots["command"] =  self.askopenfilename()
        ## ----------------------------------------------------------
        ## plots normalized
        self.plots_norm = tk.BooleanVar()
        self.plots_norm.set(False)
        self.plots_n = tk.Checkbutton(self,text ='Normalized plots',variable = self.plots_norm)
        self.plots_n.grid(row=4, column=2,sticky=tk.W)
        # self.plots
        # \todo ficar per defecte True
        # self.plots["command"] =  self.askopenfilename()
        ###################################################################
        # max dimension to compute persistent homology
        self.lab_dim_max = tk.Label(self,text="Max dimension to compute\n persistent homology",
            fg = "blue",bg = "white",font = "Verdana 10 bold")
        self.lab_dim_max.grid(row=2, column=0)
        self.var_dim = tk.IntVar(None,1)
        self.dim_max0 = tk.Radiobutton(self, text="0", variable=self.var_dim, value=0)
        self.dim_max0.grid(row=3, column=0)
        self.dim_max1 = tk.Radiobutton(self, text="1", variable=self.var_dim, value=1)
        self.dim_max1.grid(row=4, column=0)
        self.dim_max2 = tk.Radiobutton(self, text="2", variable=self.var_dim, value=2)
        self.dim_max2.grid(row=5, column=0)
        ##################################################################

    def launch_computation(self):
        print 'launching...'
        # \TODO fer funcio q converteixi les variables
        main_test(a=4,b=[1,4],
            plots_norm=self.plots_norm.get(),
            plots=self.plots_on.get(),
            max_dim=self.var_dim.get(),
            format_file=self.var_format.get(),
            data_path=self.folder_path_input.get(),
            output_path = self.folder_path_output.get(),
            file_name = self.file_path_input.get()
            )

# (data_path,format_type,file_name=None,lower_matrix = False, upper_matrix = False, output_path=None,plots_on=True,normalized=False,max_dim=1):


root = tk.Tk()
app = Application(master=root)
app.mainloop()

