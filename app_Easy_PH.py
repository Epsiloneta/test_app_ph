import Tkinter as tk

from function_main import main_test

# from Tkinter import Tk
# from tkFileDialog import askopenfilename

# # https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
# Tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# print(filename)


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.initUI()

    def initUI(self):
      
        self.master.title("Easy Persistent Homology")
        # self.pack(fill=tk.BOTH, expand=1)
        # self.pack()
        self.grid(row=0,column=0,columnspan=4,rowspan=6)
        self.createWidgets()
        self.createWidgets_optional()

    def createWidgets(self):
        
        self.data_path = tk.Button(self)
        self.data_path["text"] = "Folder data or Folder to analyse data"
        self.data_path["fg"]   = "black"
        # self.data_path["command"] =  self.askopenfilename()
        # self.data_path.pack({"side": "left"})
        self.data_path.grid(row=0, column=0)

        ## select format files
        self.lab_format_files = tk.Label(self,text="Format file/s")
        self.lab_format_files.grid(row=1, column=1)
        self.format_file = tk.Listbox(self)
        for item in ["gpickle", "npy", "txt","csv","txt (lower dist-matrix)","txt (upper dist-matrix)"]:
            self.format_file.insert(tk.END, item)
        # self.format_file["command"] =  self.askopenfilename()
        self.format_file.grid(row=2, column=1)

        ## Execute programm button ##
        self.execute_button = tk.Button(self,command=self.launch_computation)
        self.execute_button["text"] = "Run programm"
        self.execute_button["fg"]   = "blue"
        # self.data_path.pack({"side": "left"})
        self.execute_button.grid(row=0, column=3)
        ## ----------------------------------------------------------

    def createWidgets_optional(self):
        ## label results 
        self.lab_results = tk.Label(self,text="Results")
        self.lab_results.grid(row=1, column=2)
        ## ------------- OPTIONAL ----------------------------------
        ## select specific file to analyse
        self.data_file = tk.Button(self)
        self.data_file["text"] = "File to analyse"
        self.data_file["fg"]   = "black"
        # self.data_file["command"] =  self.askopenfilename()
        self.data_file.grid(row=0, column=1)
        ## ----------------------------------------------------------
        ## output data path
        self.output_folder = tk.Button(self)
        self.output_folder["text"] = "Output folder"
        self.output_folder["fg"]   = "black"
        # self.output_folder["command"] =  self.askopenfilename()
        self.output_folder.grid(row=0, column=2)
        ## ----------------------------------------------------------
        ## generate plots
        self.plots_on = tk.BooleanVar()
        self.plots_on.set(True)
        self.plots = tk.Checkbutton(self,text ='Generate Plots',variable = self.plots_on)
        self.plots.grid(row=2, column=2)
        # self.plots
        # \todo ficar per defecte True
        # self.plots["command"] =  self.askopenfilename()
        ## ----------------------------------------------------------
        ## plots normalized
        self.plots_norm = tk.BooleanVar()
        self.plots_norm.set(False)
        self.plots_n = tk.Checkbutton(self,text ='Normalized plots',variable = self.plots_norm)
        self.plots_n.grid(row=3, column=2)
        # self.plots
        # \todo ficar per defecte True
        # self.plots["command"] =  self.askopenfilename()


        ## ----------------------------------------------------------
        ## max dimension to compute persistent homology
        self.lab_dim_max = tk.Label(self,text="Max dimension to compute\n persistent homology")
        self.lab_dim_max.grid(row=1, column=0)
        # \TODO change listboxes to radiobuttons: http://www.tkdocs.com/tutorial/widgets.html
        self.list_dim_max = tk.Listbox(self)
        self.list_dim_max.grid(row=2, column=0)
        for item in ["0", "1", "2"]:
            self.list_dim_max.insert(tk.END, item)
        # \todo get active dim 1

    def launch_computation(self):
        print 'launching...'

        # get maximum dimension
        #index = self.list_dim_max.curselection()
        #dim_max = self.list_dim_max.get(index)
        dim_max = 0
        # get format file
        index = self.format_file.curselection()
        format_file = self.format_file.get(index)

        main_test(a=4,b=[1,4],
            plots_norm=self.plots_norm.get(),
            plots=self.plots_on.get(),
            max_dim=dim_max,
            format_file=format_file
            )



root = tk.Tk()
app = Application(master=root)
app.mainloop()

