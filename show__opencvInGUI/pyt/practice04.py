import os, sys, inspect
import cv2
import numpy       as np
import tkinter     as tk
import tkinter.ttk as ttk
import matplotlib.pyplot                 as plt
import matplotlib.backends.backend_tkagg as btk


# ========================================================= #
# ===  define_gui                                       === #
# ========================================================= #
def define__gui( title="gui", width=None, height=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( width is None ):
        width  = 400
        print( "[define__gui.py] default  {0:12} : {1}   is used.".format( "width" , width  ) )
    if ( height is None ):
        height = 800
        print( "[define__gui.py] default  {0:12} : {1}   is used.".format( "height", height ) )
        
    # ------------------------------------------------- #
    # --- [2] define gui application                --- #
    # ------------------------------------------------- #
    frame = tk.Tk()
    frame.title   ( title )
    frame.geometry( "{0}x{1}".format( width, height ) )
    gui__template( frame, width=width, height=height )
    frame.mainloop()
    return()


# ========================================================= #
# ===  gui__template.py                                 === #
# ========================================================= #

class gui__template( ttk.Frame ):
    
    # ========================================================= #
    # ===  initialize                                       === #
    # ========================================================= #
    def __init__( self, root=None, width=400, height=800 ):
        super().__init__( root, width=width, height=height, \
                          borderwidth=3, relief="groove" )
        self.root        = root
        self.widgets     = {}
        self.params      = {}
        self.values      = {}
        self.posits      = {}
        self.functions   = {}
        self.Menu_Entity = None
        self.Menus       = {}
        self.pack()
        self.pack_propagate(0) # to stop shrinking into minimum size.
        self.create__widgets()
        keys = [ "opencv" ]
        self.functions["plot"]   = self.draw__matplotlibWindow
        self.functions["opencv"] = self.draw__opencv2Window
        for key in keys:
            self.set__matplotlibWindow( key=key )
        self.define__positionsOfWidgets()
        self.place__widgets( verbose=True )

        
    # ========================================================= #
    # ===  create widgets                                   === #
    # ========================================================= #
    def create__widgets( self ):

        # ------------------------------------------------- #
        # --- [1] Entry widgets                         --- #
        # ------------------------------------------------- #
        #  -- for multi line text input,                --  #
        #  --    use tk.Text, instead                   --  #
        # ------------------------------------------------- #
        self.widgets["Entry01"] = ttk.Entry( self )

        # ------------------------------------------------- #
        # --- [2] Button widgets                        --- #
        # ------------------------------------------------- #
        self.functions["Button01"] = self.function
        self.widgets  ["Button01"] = ttk.Button( self, text="update", \
                                                 command=self.functions["Button01"] )
        
        # ------------------------------------------------- #
        # --- [3] Label widgets                         --- #
        # ------------------------------------------------- #
        #  -- for multi line message,                   --  #
        #  --    use tk.Message, instead                --  #
        # ------------------------------------------------- #
        self.widgets["Label01"] = ttk.Label( self, text="Label", width=200 )

        # ------------------------------------------------- #
        # --- [4] Checkbutton widgets                   --- #
        # ------------------------------------------------- #
        self.values ["Checkbutton01"] = tk.BooleanVar()
        self.widgets["Checkbutton01"] = ttk.Checkbutton( self, text="Checkbutton", \
                                                         variable=self.values["Checkbutton01"] )
        
        # ------------------------------------------------- #
        # --- [5] Radiobutton widgets                   --- #
        # ------------------------------------------------- #
        key   = "Radiobutton01"
        items = { "A":"A", "B":"B", "C":"C" }
        self.values [key]  = tk.StringVar()
        self.params [key]  = items
        for ik,item_key in enumerate( self.params[key].keys() ):
            wkey               = "{0}-{1}".format( key, item_key )
            text,value         =  item_key, self.params[key][item_key] 
            self.widgets[wkey] = ttk.Radiobutton( self, text=text, value=value,\
                                                  variable=self.values[key] )

        # ------------------------------------------------- #
        # --- [6] Combobox widgets                      --- #
        # ------------------------------------------------- #
        self.values ["Combobox01"] = tk.StringVar()
        self.params ["Combobox01"] = [ "type-A", "type-B", "type-C" ]
        self.widgets["Combobox01"] = ttk.Combobox( self, textvariable=self.values["Combobox01"],\
                                                   values=self.params["Combobox01"] )

        # ------------------------------------------------- #
        # --- [7] Scale widgets                         --- #
        # ------------------------------------------------- #
        self.values ["Scale01"] = tk.DoubleVar()
        self.params ["Scale01"] = [ 0, 10 ]
        self.widgets["Scale01"] = ttk.Scale( self, variable=self.values["Scale01"], \
                                             orient=tk.HORIZONTAL, length=200, \
                                             from_=self.params["Scale01"][0], \
                                             to_  =self.params["Scale01"][1], \
                                             command=self.draw__matplotlibWindow )
        
        # ------------------------------------------------- #
        # --- [8] File Dialog Box Button                --- #
        # ------------------------------------------------- #
        self.widgets["FileDialog01"] = ttk.Button( self, text="Open File",\
                                                   command=self.open__fileDialogBox )
        
        # ------------------------------------------------- #
        # --- [10] menu widgets                         --- #
        # ------------------------------------------------- #
        self.Menu_Entity     = tk.Menu( self.root )
        self.Menus["menu01"] = tk.Menu( self.Menu_Entity, tearoff=False )
        self.Menus["menu01"].add_command( label="command01", command=self.function )
        self.Menus["menu01"].add_command( label="command02", command=self.function )
        self.Menus["menu02"] = tk.Menu( self.Menu_Entity, tearoff=False )
        self.Menus["menu02"].add_command( label="command01", command=self.function )
        self.Menus["menu02"].add_command( label="command02", command=self.function )
        self.Menu_Entity.add_cascade( label="menu01", menu=self.Menus["menu01"] )
        self.Menu_Entity.add_cascade( label="menu02", menu=self.Menus["menu02"] )
        self.root.config( menu=self.Menu_Entity )
        return()


    # ========================================================= #
    # ===  define position of the widgets                   === #
    # ========================================================= #
    def define__positionsOfWidgets( self ):

        # posits (list) :: [ relx, rely, relwidth, relheight, anchor ]
        
        # ------------------------------------------------- #
        # --- [1] specify position directory            --- #
        # ------------------------------------------------- #
        self.posits ["Entry01"]          = [  0.05, 0.05, 0.5 , None ]
        self.posits ["Button01"]         = [  0.65, 0.05, 0.3 , None ]
        self.posits ["Label01"]          = [  0.1,  0.10, 0.5 , None ]
        self.posits ["Checkbutton01"]    = [  0.65, 0.10, 0.3 , None ]
        self.posits ["Radiobutton01-A"]  = [  0.10, 0.15, 0.1 , None ]
        self.posits ["Radiobutton01-B"]  = [  0.25, 0.15, 0.1 , None ]
        self.posits ["Radiobutton01-C"]  = [  0.40, 0.15, 0.1 , None ]
        self.posits ["Combobox01"]       = [  0.60, 0.15, 0.35, None ]
        self.posits ["Scale01"]          = [  0.10, 0.20, 0.80, None ]
        self.posits ["FileDialog01"]     = [  0.65, 0.25, 0.3 , None ]
        self.posits ["opencv"]           = [  0.1,  0.6, 0.8, 0.3 ]

        return()
    
    
    # ========================================================= #
    # ===  place widgets ( relative position )              === #
    # ========================================================= #
    def place__widgets( self, verbose=True, anchor_default=tk.NW ):

        into_tkAnchor = { "w" :tk.W , "e" :tk.E , "s" :tk.N , "n" :tk.N , "center":tk.CENTER, \
                          "sw":tk.SW, "se":tk.SE, "nw":tk.NW, "ne":tk.NE }
        
        # ------------------------------------------------- #
        # --- [1] for every widgets place               --- #
        # ------------------------------------------------- #
        common_keys   = set( self.widgets.keys() ) & set( self.posits.keys() )
        not_specified = set( self.widgets.keys() ) - set( self.posits.keys() )
        if ( verbose ):
            print( "\n\n" + "[define__gui.place__widgets] common keys   :: " )
            for ik,key in enumerate( common_keys   ):
                print( "     {0:15}".format( key ), end="" )
                if ( (ik+1)%3 == 0 ): print()
                
            print( "\n\n" + "[define__gui.place__widgets] not specified :: " )
            for ik,key in enumerate( not_specified ):
                print( "     {0:15}".format( key ), end="" )
                if ( (ik+1)%3 == 0 ): print()
            print()
    
        # ------------------------------------------------- #
        # --- [2] place widgets                         --- #
        # ------------------------------------------------- #
        for ik,key in enumerate( common_keys ):
            posits = self.posits[key]

            # ------------------------------------------------- #
            # --- [2-1] irregular value check               --- #
            # ------------------------------------------------- #
            if   ( len( posits ) == 5 ):
                pass
            elif ( len( posits ) == 4 ):
                posits += [ anchor_default ]
            elif ( len( posits ) == 3 ):
                posits += [ None, anchor_default ]
            elif ( len( posits ) == 2 ):
                posits += [ None, None, anchor_default ]
            else:
                print( "[define__gui.py::place__widgets] unknown posits..." )
                print( "[define__gui.py::place__widgets] ", posits )
                sys.exit()
            if ( type( posits[4] ) is None ):
                posits[4] = anchor_default
            if ( type( posits[4] ) is str ):
                try:
                    posits[4] = into_tkAnchor[ ( posits[4] ).lower() ]
                except KeyError:
                    print( "[define__gui.py::place__widgets] unknown anchor:(posits[4])..." )
                    print( "[define__gui.py::place__widgets] ", posits )
                    sys.exit()
            if ( not( posits[4] in into_tkAnchor.values() ) ):
                print( "[define__gui.py::place__widgets] unknown posits..." )
                print( "[define__gui.py::place__widgets] ", posits )
                sys.exit()
                
            # ------------------------------------------------- #
            # --- [2-2] actual placement                    --- #
            # ------------------------------------------------- #
            relx, rely, relw, relh, anchor = posits
            self.widgets[key].place( relx=relx, rely=rely, \
                                     relwidth=relw, relheight=relh, anchor=anchor )
        return()
        
    # ========================================================= #
    # ===  some function                                    === #
    # ========================================================= #
    def function( self ):
        print( "[gui__template] Nothing to do. Function " )
        return()


    # ========================================================= #
    # ===  open__fileDialogBox                              === #
    # ========================================================= #
    def open__fileDialogBox( self, event=None, filetypes=[("","*")], getDirectoryPath=False, \
                             tkString=False, returnType="path" ):
    
        # ------------------------------------------------- #
        # --- [1] arguments                             --- #
        # ------------------------------------------------- #
        if   ( type( filetypes ) is str ):
            filetypes = [ filetypes ]
        elif ( type( filetypes ) is list ):
            pass
        else:
            filetypes = ["","*"]

        # ------------------------------------------------- #
        # --- [2] call file dialog box                  --- #
        # ------------------------------------------------- #
        import tkinter.filedialog as dialog
        initDir  = os.path.abspath( os.path.dirname( __file__ ) )
        if ( getDirectoryPath ):
            path = dialog.askdirectory   ( initialdir=initDir )
        else:
            path = dialog.askopenfilename( initialdir=initDir, filetypes=filetypes )

        # ------------------------------------------------- #
        # --- [3] store in tkString                     --- #
        # ------------------------------------------------- #
        if   ( tkString is None ):
            tkString = None
        elif ( ( type( tkString ) is bool ) and ( tkString is True ) ):
            tkString = tk.StringVar()
        elif (   type( tkString ) is type( tk.StringVar() ) ):
            pass
        else:
            tkString = None
        if ( tkString is not None ):
            if ( len( path ) == 0 ):
                tkString.set( "No file selection :: cancelled...." )
            else:
                tkString.set( path )

        # ------------------------------------------------- #
        # --- [3] return type                           --- #
        # ------------------------------------------------- #
        if   ( returnType.lower() == "path" ):
            return( path )
        elif ( returnType.lower() == "tk"   ):
            return( tkString )
        elif ( returnType.lower() == "both" ):
            return( path, tkString )
        else:
            return( path )


    # ========================================================= #
    # ===  set__matplotlibWindow                            === #
    # ========================================================= #
    def set__matplotlibWindow( self, key=None ):
        if ( key is None ): sys.exit( "[set__matplotlibWindow] key == ???" )
        fig, ax            = list( plt.subplots( tight_layout=True ) )
        # ax.set_xticks     ( np.round( np.linspace(  0.0, 1.0, 6 ), 2 ) )
        # ax.set_yticks     ( np.round( np.linspace(  0.0, 1.0, 6 ), 2 ) )
        # ax.set_xticklabels( np.round( np.linspace(  0.0, 1.0, 6 ), 2 ), fontsize=6 )
        # ax.set_yticklabels( np.round( np.linspace(  0.0, 1.0, 6 ), 2 ), fontsize=6 )
        # ax.set_xlim( 0.0, 1.0 )
        # ax.set_ylim( 0.0, 1.0 )
        canvas             = btk.FigureCanvasTkAgg( fig, self.root )
        plot_entity,       = ax.plot( [], [], color="RoyalBlue", linewidth=1.2 )
        self.values [key]  = [ fig, ax, plot_entity, canvas ]
        self.widgets[key]  = canvas.get_tk_widget()
        self.functions[key]()


    # ========================================================= #
    # ===  draw__matplotlib                                 === #
    # ========================================================= #
    def draw__matplotlibWindow( self, event=None ):
        widgets_key   = "plot"
        params_key    = "Scale01"
        a             = self.widgets[params_key].get()
        x             = np.linspace( 0.0, 1.0, 101 )
        y             = x**a
        pE, canvas    = ( self.values[widgets_key] )[2:]
        pE.set_data( x, y )
        canvas.draw()


    # ========================================================= #
    # ===  draw__opencv                                     === #
    # ========================================================= #
    def draw__opencv2Window( self, event=None ):
        widgets_key   = "opencv"
        jpgFile       = "jpg/lena.jpg"
        img_bgr       = cv2.imread( jpgFile )
        img_rgb       = cv2.cvtColor( img_bgr, cv2.COLOR_BGR2RGB ) # BGRからRGBに変換
        ax,_,canvas   = ( self.values[widgets_key] )[1:]
        ax.imshow( img_rgb )
        canvas.draw()

    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    define__gui()
