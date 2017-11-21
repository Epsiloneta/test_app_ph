import Tkinter as tk


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
        self.grid(row=0,column=0,columnspan=3,rowspan=4)
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
        for item in ["gpickle", "npy", "txt","csv"]:
            self.format_file.insert(tk.END, item)
        # self.format_file["command"] =  self.askopenfilename()
        self.format_file.grid(row=2, column=1)
        ## ----------------------------------------------------------

    def createWidgets_optional(self):
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
        plots_on = tk.BooleanVar()
        plots_on.set(True)
        self.plots = tk.Checkbutton(self,text ='Generate Plots',variable = plots_on)
        self.plots.grid(row=3, column=0)
        # self.plots
        # \todo ficar per defecte True
        # self.plots["command"] =  self.askopenfilename()
        ## ----------------------------------------------------------
        ## plots normalized
        plots_norm = tk.BooleanVar()
        plots_norm.set(True)
        self.plots_n = tk.Checkbutton(self,text ='Normalized plots',variable = plots_norm)
        self.plots_n.grid(row=4, column=0)
        # self.plots
        # \todo ficar per defecte True
        # self.plots["command"] =  self.askopenfilename()


        ## ----------------------------------------------------------
        ## max dimension to compute persistent homology
        self.lab_dim_max = tk.Label(self,text="Max dimension to compute\n persistent homology")
        self.lab_dim_max.grid(row=1, column=0)
        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=2, column=0)
        for item in ["0", "1", "2"]:
            self.listbox.insert(tk.END, item)
        # \todo get active dim 1



root = tk.Tk()
app = Application(master=root)
app.mainloop()

