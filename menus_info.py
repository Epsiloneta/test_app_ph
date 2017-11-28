import Tkinter as tk

from help_dialogs import CustomText

# \todo add references
def about_homology():
    win = tk.Toplevel()
    win.title("Homology and Persistent Homology")
    about = '''

          -------------------------------------------------------------------
          HOMOLOGY
          -------------------------------------------------------------------
          Homology counts the n-dimensional holes in a given space. 

          How to interpret holes?

          0-dimensional holes: represent connected components
          1-dimensional holes: represent cycles
          2-dimensional holes: represent voids
          n-dimensional holes: represent cavities of n-dimension

          The number of holes (how many) given a dimension is called: betti numbers 
          (betti0: how many connected components there are, betti1: how many cycles there are, ...). 

          Obs: if our space or our object is embedded (lives) in dimension 3 we can not have holes of higher dimension than 2.

          Examples:
            * Sphere:           
              number of 0-dimensional holes: 1
              number of 1-dimensional holes: 0
              number of 2-dimensional holes: 1
              number of n-dimensional holes with n>2: 0 (for all n>2)

            * Torus (also well known as a empty donut):
              number of 0-dimensional holes: 1
              number of 1-dimensional holes: 2
              number of 2-dimensional holes: 1
              number of n-dimensional holes with n>2: 0 (for all n>2)

          How to compute it?

          Go to... 

          -------------------------------------------------------------------
          PERSISTENT HOMOLOGY
          -------------------------------------------------------------------
          Persistent Homology (PH) counts the evolution of n-dimensional holes in a given space.
          'n' refers to the dimension of the hole.

          Filtration: a set of datasets (set1 contained in set2, contained in set3, ... ) from our original dataset.
          
          Example (a): 
            Given a weighted network, G, that respresent a distances between pairs, we can consider all possible thresholds, 
            then we will obtain a set of networks.

            Adjacency matrix of G = [[0,1,3,4],[1,0,10,2],[3,10,0,3],[4,2,3,0]]

            step 0: threshold = 0 -> all nodes disconnected -> betti_0 = 4, betti_1 = 0, betti_n = 0 for n>1
            step 1: threshold = 1 -> appears edge (0,1) ->  betti_0 = 3, betti_1 = 0, betti_n = 0 for n>1
            step 2: threshold = 2 -> appears edge (1,3) ->  betti_0 = 2, betti_1 = 0, betti_n = 0 for n>1
            step 3: threshold = 3 -> appears edges (0,2) and (2,3) ->  betti_0 = 1, betti_1 = 1, betti_n = 0 for n>1 
            (here a cycle appears and we already have an unique connected component)
            step 4: threshold = 4 -> appears edge (0,3) ->  betti_0 = 1, betti_1 = 0, betti_n = 0 for n>1 
            (here the cycle disappears (a triangle is considered full, then it is not a cycle) and we continue to have an unique connected component)
            step 5: threshold > 10 -> appears edge (1,2) ->  betti_0 = 1, betti_1 = 0, betti_n = 0 for n>1 

          It is possible define a parametrization of betti numbers (defined above), that how many holes (for each dimension) there are for each step in the filtration.
          But, there are a better and more informative feature obtained from PH: persistence diagrams or equivalently barcodes.

          Persistence diagrams: set of (x,y) points where,
             x: step/threshold where a n-dim hole is born
             y: step/threshold where a n-dim hole is died

          Barcode:
            Bars of lenght (y-x) indicating when a n-dim hols has been born and died.

          Persistence diagram (PD) from example (a) accoring threshold units:
            0-dimensional PD:
                  points = {(0,1),(0,2),(0,3),(0,)} # (0,) or (0,10) indicates that the one connected component persist forever in the filtration.
            1-dimensional PD:
                  points = {(4,10)} ## there is only one cycle that apperas at threshold >= 4 and then dissapear at threshold = 10
          
          Interpretation (go to Persistent Homology Interpretation to know more about):

            Persistence diagram: as farther a point is from the diagonal more persistent is.
            Barcodes: as larger the bar is more persistent is.

          Keywords in PH:
            * Rips-Vietoris complex filtration
            * Cech complex filtration
            * Clique complex
            * Simplicial complex


          How to compute it?

          Go to... 
        '''
    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    # t.HighlightPattern("Homology", "blue")
    # t.HighlightPattern("Persistent Homology", "blue")
    # t.HighlightPattern("0-dimensional holes", "blue")
    # t.HighlightPattern("1-dimensional holes", "blue")
    # t.HighlightPattern("2-dimensional holes", "blue")
    # tk.Button(win, text='OK', command=win.destroy).pack()

def about_persistent_homology_interpret():
    win = tk.Toplevel()
    win.title("About Persistent Homology interpretation and comparison")
    about = '''

          Persistent Homology can give an idea of the shape of the data.
          
          How? Knowing when connected components, cycles and voids appear and disappear and how many we have.

          Main shapes are that live longer across the filtration.

          For example: Persistence diagrams can help in shape classification.

          Some applications:

          Go to... 


          Compare persistence diagrams:
            * qth Wasserstein distance
            * Bottleneck distance
            * Persistence landscape (Bubenik 2012 and 2015).
            * Vineyards
            * Similarity Kernel (Reininhaus et al 2015)


        '''
    # about = re.sub("\n\s*", "\n", about) # remove leading whitespace from each line
    t=CustomText(win, wrap="word", width=100, height=25, borderwidth=0)
    t.tag_configure("blue", foreground="blue")
    t.pack(sid="top",fill="both",expand=True)
    t.insert("1.0", about)
    # t.HighlightPattern("Homology", "blue")
    # t.HighlightPattern("Persistent Homology", "blue")
    # t.HighlightPattern("0-dimensional holes", "blue")
    # t.HighlightPattern("1-dimensional holes", "blue")
    # t.HighlightPattern("2-dimensional holes", "blue")
    # tk.Button(win, text='OK', command=win.destroy).pack()