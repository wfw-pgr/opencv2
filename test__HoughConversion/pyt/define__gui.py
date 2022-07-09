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
        # ------------------------------------------------- #
        # --- [1] variables                             --- #
        # ------------------------------------------------- #
        self.root        = root
        self.widgets     = {}
        self.params      = {}
        self.values      = {}
        self.labels      = {}
        self.posits      = {}
        self.functions   = {}
        self.Menu_Entity = None
        self.Menus       = {}
        # ------------------------------------------------- #
        # --- [2] set values                            --- #
        # ------------------------------------------------- #
        self.set__values()
        self.set__params()
        self.set__labels()
        self.set__functions()
        self.set__positions()
        # ------------------------------------------------- #
        # --- [3] widgets                               --- #
        # ------------------------------------------------- #
        self.create__widgets()
        self.set__matplotlibWindow( key="opencv" )
        # ------------------------------------------------- #
        # --- [4] placemant                             --- #
        # ------------------------------------------------- #
        self.place__widgets( verbose=True )
        self.pack_propagate( False ) # to stop shrinking into minimum size.
        self.pack()


    # ========================================================= #
    # ===  set values                                       === #
    # ========================================================= #
    def set__values( self ):

        # ------------------------------------------------- #
        # ---   store default values                    --- #
        # ------------------------------------------------- #
        self.values["opencv"] = None

        return()
        
    # ========================================================= #
    # ===  set function name                                === #
    # ========================================================= #
    def set__functions( self ):

        # ------------------------------------------------- #
        # ---   store associated function name          --- #
        # ------------------------------------------------- #
        self.functions["Button01"] = self.draw__opencvWindow
        self.functions["Adjust01"] = self.update__opencvWindow
        self.functions["Adjust02"] = self.update__opencvWindow
        self.functions["Adjust03"] = self.update__opencvWindow
        self.functions["opencv"]   = self.draw__opencvWindow
        self.functions["FileOpen01.button"] = self.load__fileButton
        self.functions["FileOpen01.dialog"] = self.load__fileDialog

        return()


    # ========================================================= #
    # ===  set Parameters                                   === #
    # ========================================================= #
    def set__params( self ):

        # ------------------------------------------------- #
        # ---   store parameters to be used             --- #
        # ------------------------------------------------- #
        #   < params > [ min, max, init, increment ]   #
        self.params["Spinbox01"]   = [ 0, 255,  90,   1 ]  
        self.params["Spinbox02"]   = [ 0, 255, 110,   1 ] 
        self.params["Spinbox03"]   = [ 0,   5, 1.5, 0.1 ]
        self.params["Adjust01"]    = [ 0, 200, 110,   1 ]
        self.params["Adjust02"]    = [ 0, 200,  20,   1 ]
        self.params["Adjust03"]    = [ 0, 200, 120,   1 ]
        self.params["opencv"]      = None
        
        return()


    # ========================================================= #
    # ===  set label name                                   === #
    # ========================================================= #
    def set__labels( self ):

        # ------------------------------------------------- #
        # ---   store lable for each widget             --- #
        # ------------------------------------------------- #
        self.labels["Spinbox01"]   = "threshold1"
        self.labels["Spinbox02"]   = "threshold2"
        self.labels["Spinbox03"]   = "dp"
        self.labels["Adjust01"]    = "min_Distance"
        self.labels["Adjust02"]    = "min_Radius"
        self.labels["Adjust03"]    = "max_Radius"
        self.labels["FileOpen01.button"] = "Load"
        self.labels["FileOpen01.dialog"] = "Open File"

        return()


    # ========================================================= #
    # ===  set position of the widgets                      === #
    # ========================================================= #
    def set__positions( self ):

        # posits (list) :: [ relx, rely, relwidth, relheight, anchor ]
        
        # ------------------------------------------------- #
        # ---     specify position directory            --- #
        # ------------------------------------------------- #
        self.posits ["FileOpen01.entry"]  = [  0.05, 0.03, 0.70, None ]
        self.posits ["FileOpen01.button"] = [  0.77, 0.03, 0.18, None ]
        self.posits ["FileOpen01.dialog"] = [  0.05, 0.07, 0.90, None ]
        self.posits ["Spinbox01"]         = [  0.05, 0.13, 0.20, None ]
        self.posits ["Spinbox01.label"]   = [  0.05, 0.11, 0.20, None ]
        self.posits ["Spinbox02"]         = [  0.40, 0.13, 0.20, None ]
        self.posits ["Spinbox02.label"]   = [  0.40, 0.11, 0.20, None ]
        self.posits ["Spinbox03"]         = [  0.75, 0.13, 0.20, None ]
        self.posits ["Spinbox03.label"]   = [  0.75, 0.11, 0.20, None ]
        self.posits ["Adjust01.label"]    = [  0.50, 0.22, 0.90, 0.08, "center" ]
        self.posits ["Adjust01.scale"]    = [  0.08, 0.22, 0.68, None ]
        self.posits ["Adjust01.spinb"]    = [  0.78, 0.22, 0.16, None ]
        self.posits ["Adjust02.label"]    = [  0.50, 0.32, 0.90, 0.08, "center" ]
        self.posits ["Adjust02.scale"]    = [  0.08, 0.32, 0.68, None ]
        self.posits ["Adjust02.spinb"]    = [  0.78, 0.32, 0.16, None ]
        self.posits ["Adjust03.label"]    = [  0.50, 0.42, 0.90, 0.08, "center" ]
        self.posits ["Adjust03.scale"]    = [  0.08, 0.42, 0.68, None ]
        self.posits ["Adjust03.spinb"]    = [  0.78, 0.42, 0.16, None ]
        self.posits ["opencv"]            = [  0.1,  0.50, 0.80, 0.45 ]
        return()

    
    # ========================================================= #
    # ===  create widgets                                   === #
    # ========================================================= #
    def create__widgets( self ):

        # ------------------------------------------------- #
        # --- [1] File Open Set                         --- #
        # ------------------------------------------------- #
        key                = "FileOpen01"
        ekey, bkey, dkey   = [ key+suffix for suffix in [ ".entry", ".button", ".dialog" ] ]
        self.values [key]  = tk.StringVar()
        self.widgets[ekey] = ttk.Entry( self, textvariable=self.values[key] )
        self.widgets[bkey] = ttk.Button( self, text=self.labels[bkey], \
                                         command=self.functions[bkey] )
        self.widgets[dkey] = ttk.Button( self, text=self.labels[dkey],\
                                         command=self.functions[dkey] )

        # ------------------------------------------------- #
        # --- [3] spinbox for parameters                --- #
        # ------------------------------------------------- #
        min_,max_,ini_,inc_ = 0, 1, 2, 3
        key                 = "Spinbox01"
        lkey                = "{}.label".format( key )
        self.widgets[lkey]  = ttk.Label( self, text=self.labels[key] )
        self.values [key]   = tk.StringVar()
        self.values [key].set( str( self.params[key][ini_] ) )
        self.widgets[key]   = ttk.Spinbox( self, state="readonly", \
                                           textvariable=self.values[key], \
                                           from_       =self.params[key][min_], \
                                           to_         =self.params[key][max_], \
                                           increment   =self.params[key][inc_]  )
        
        # ------------------------------------------------- #
        # --- [4] spinbox for parameters 2              --- #
        # ------------------------------------------------- #
        min_,max_,ini_,inc_ = 0, 1, 2, 3
        key                 = "Spinbox02"
        lkey                = "{}.label".format( key )
        self.widgets[lkey]  = ttk.Label( self, text=self.labels[key] )
        self.values [key]   = tk.StringVar()
        self.values [key].set( str( self.params[key][ini_] ) )
        self.widgets[key]   = ttk.Spinbox( self, state="readonly", \
                                           textvariable=self.values[key], \
                                           from_       =self.params[key][min_], \
                                           to_         =self.params[key][max_], \
                                           increment   =self.params[key][inc_]  )

        # ------------------------------------------------- #
        # --- [5] spinbox for parameters 3              --- #
        # ------------------------------------------------- #
        min_,max_,ini_,inc_ = 0, 1, 2, 3
        key                 = "Spinbox03"
        lkey                = "{}.label".format( key )
        self.widgets[lkey]  = ttk.Label( self, text=self.labels[key] )
        self.values [key]   = tk.StringVar()
        self.values [key].set( str( self.params[key][ini_] ) )
        self.widgets[key]   = ttk.Spinbox( self, state="readonly", \
                                           textvariable=self.values[key], \
                                           from_       =self.params[key][min_], \
                                           to_         =self.params[key][max_], \
                                           increment   =self.params[key][inc_]  )

        # ------------------------------------------------- #
        # --- [6] adjust set widgets                    --- #
        # ------------------------------------------------- #
        key                 = "Adjust01"
        min_,max_,ini_,inc_ = 0, 1, 2, 3
        borderwidth         = 8
        lkey,sckey,spkey    = [ key+suffix for suffix in [ ".label", ".scale", ".spinb" ] ]
        self.widgets[lkey]  = ttk.LabelFrame( self, text=self.labels[key], \
                                             borderwidth=borderwidth, labelanchor=tk.N )
        self.values [key]   = tk.StringVar()
        self.values [key].set( str( self.params[key][ini_] ) )
        self.widgets[sckey] = ttk.Scale  ( self, variable=self.values[key], \
                                           orient        =tk.HORIZONTAL, \
                                           from_         =self.params[key][min_], \
                                           to_           =self.params[key][max_], \
                                           command       =self.functions[key] )
        self.widgets[spkey] = ttk.Spinbox( self, state   ="readonly", \
                                           textvariable  =self.values[key], \
                                           from_         =self.params[key][min_], \
                                           to_           =self.params[key][max_], \
                                           increment     =self.params[key][inc_], \
                                           command       =self.functions[key] )
        
        # ------------------------------------------------- #
        # --- [7] adjust set widgets                    --- #
        # ------------------------------------------------- #
        key                 = "Adjust02"
        min_,max_,ini_,inc_ = 0, 1, 2, 3
        borderwidth         = 8
        lkey,sckey,spkey    = [ key+suffix for suffix in [ ".label", ".scale", ".spinb" ] ]
        self.widgets[lkey]  = ttk.LabelFrame( self, text=self.labels[key], \
                                             borderwidth=borderwidth, labelanchor=tk.N )
        self.values [key]   = tk.StringVar()
        self.values [key].set( str( self.params[key][ini_] ) )
        self.widgets[sckey] = ttk.Scale  ( self, variable=self.values[key], \
                                           orient        =tk.HORIZONTAL, \
                                           from_         =self.params[key][min_], \
                                           to_           =self.params[key][max_], \
                                           command       =self.functions[key] )
        self.widgets[spkey] = ttk.Spinbox( self, state   ="readonly", \
                                           textvariable  =self.values[key], \
                                           from_         =self.params[key][min_], \
                                           to_           =self.params[key][max_], \
                                           increment     =self.params[key][inc_], \
                                           command       =self.functions[key] )
        
        # ------------------------------------------------- #
        # --- [8] adjust set widgets                    --- #
        # ------------------------------------------------- #
        key                 = "Adjust03"
        min_,max_,ini_,inc_ = 0, 1, 2, 3
        borderwidth         = 8
        lkey,sckey,spkey    = [ key+suffix for suffix in [ ".label", ".scale", ".spinb" ] ]
        self.widgets[lkey]  = ttk.LabelFrame( self, text=self.labels[key], \
                                             borderwidth=borderwidth, labelanchor=tk.N )
        self.values [key]   = tk.StringVar()
        self.values [key].set( str( self.params[key][ini_] ) )
        self.widgets[sckey] = ttk.Scale  ( self, variable=self.values[key], \
                                           orient        =tk.HORIZONTAL, \
                                           from_         =self.params[key][min_], \
                                           to_           =self.params[key][max_], \
                                           command       =self.functions[key] )
        self.widgets[spkey] = ttk.Spinbox( self, state   ="readonly", \
                                           textvariable  =self.values[key], \
                                           from_         =self.params[key][min_], \
                                           to_           =self.params[key][max_], \
                                           increment     =self.params[key][inc_], \
                                           command       =self.functions[key] )
        

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
    # ===  open__fileDialogBox                              === #
    # ========================================================= #
    def open__fileDialogBox( self, event=None, filetypes=[("","*")], getDirectoryPath=False, \
                             tkString=False, returnType="path", initDir=None ):
    
        # ------------------------------------------------- #
        # --- [1] arguments                             --- #
        # ------------------------------------------------- #
        if   ( type( filetypes ) is str ):
            filetypes = [ filetypes ]
        elif ( type( filetypes ) is list ):
            pass
        else:
            filetypes = ["","*"]
        if ( initDir is None ):
            initDir  = os.path.abspath( os.path.dirname( __file__ ) )

        # ------------------------------------------------- #
        # --- [2] call file dialog box                  --- #
        # ------------------------------------------------- #
        import tkinter.filedialog as dialog
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
        # ------------------------------------------------- #
        # --- [1] Arguments                             --- #
        # ------------------------------------------------- #
        if ( key is None ):
            sys.exit( "[set__matplotlibWindow] key == ???" )
        # ------------------------------------------------- #
        # --- [2] set figure area                       --- #
        # ------------------------------------------------- #
        fig                = plt.figure()
        ax                 = fig.add_axes( [0,0,1,1] )
        canvas             = btk.FigureCanvasTkAgg( fig, self.root )
        plot_entity,       = ax.plot( [], [], color="RoyalBlue", linewidth=1.2 )
        self.values [key]  = [ fig, ax, plot_entity, canvas ]
        self.widgets[key]  = canvas.get_tk_widget()
        self.functions[key]()


    # ========================================================= #
    # ===  draw__matplotlib                                 === #
    # ========================================================= #
    def draw__matplotlibWindow( self, event=None ):
        
        # ------------------------------------------------- #
        # --- [1] function determination                --- #
        # ------------------------------------------------- #
        widgets_key   = "plot"
        params_key    = "Adjust01.scale"
        # ------------------------------------------------- #
        # --- [2] plot area                             --- #
        # ------------------------------------------------- #
        ax,pE,canvas  = ( self.values[widgets_key] )[1:]
        ax.set_position   ( [ 0.12, 0.12, 0.90, 0.90 ] )
        ax.set_xticks     ( np.round( np.linspace(  0.0, 1.0, 6 ), 2 ) )
        ax.set_yticks     ( np.round( np.linspace(  0.0, 1.0, 6 ), 2 ) )
        ax.set_xticklabels( np.round( np.linspace(  0.0, 1.0, 6 ), 2 ), fontsize=6 )
        ax.set_yticklabels( np.round( np.linspace(  0.0, 1.0, 6 ), 2 ), fontsize=6 )
        ax.set_xlim( 0.0, 1.0 )
        ax.set_ylim( 0.0, 1.0 )
        # ------------------------------------------------- #
        # --- [3] coefficient & function                --- #
        # ------------------------------------------------- #
        a             = self.widgets[params_key].get()
        x             = np.linspace( 0.0, 1.0, 101 )
        y             = x**a
        # ------------------------------------------------- #
        # --- [4] plot                                  --- #
        # ------------------------------------------------- #
        pE.set_data( x, y )
        canvas.draw()

        
    # ========================================================= #
    # ===  draw__opencv                                     === #
    # ========================================================= #
    def draw__opencvWindow( self, event=None ):

        pE_         = 2
        name_, img_ = 0, 1
        key         = "opencv"
        
        # ------------------------------------------------- #
        # --- [1] plot area                             --- #
        # ------------------------------------------------- #
        fig,ax,_,canvas = ( self.values[key] )[0:]
        ax.set_position( [ 0.05, 0.05, 0.9, 0.9 ] )
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        fig.patch.set_facecolor( "black" )
        fig.patch.set_alpha( 1.0 )
        # ------------------------------------------------- #
        # --- [2] image opencv                          --- #
        # ------------------------------------------------- #
        if ( self.params[key] is not None ):
            img_bgr             = cv2.imread  ( self.params[key][name_]    )
            img_rgb             = cv2.cvtColor( img_bgr, cv2.COLOR_BGR2RGB )
            self.params[key][1] = img_bgr
        else:
            img_rgb             = np.array( [ [0,0,0] ] )
            self.params[key]    = [ None, img_rgb ]
        self.values[key][pE_] = ax.imshow( img_rgb )
        canvas.draw()

    # ========================================================= #
    # ===  update__opencv                                   === #
    # ========================================================= #
    def update__opencvWindow( self, event=None ):

        name_, img_    = 0, 1
        key            = "opencv"

        # ------------------------------------------------- #
        # --- [1] modify opencv images                  --- #
        # ------------------------------------------------- #
        _,ax,pE,canvas = self.values[key]
        th1            =   int(        self.values["Spinbox01"].get()   )
        th2            =   int(        self.values["Spinbox02"].get()   )
        dp             =        float( self.values["Spinbox03"].get() )
        minDist        =   int( float( self.values["Adjust01" ].get() ) )
        minRadius      =   int( float( self.values["Adjust02" ].get() ) )
        maxRadius      =   int( float( self.values["Adjust03" ].get() ) )

        # ------------------------------------------------- #
        # --- [2] canny                                 --- #
        # ------------------------------------------------- #
        img_rgb        = cv2.cvtColor( self.params[key][img_], cv2.COLOR_BGR2RGB  )
        img_gray       = cv2.cvtColor( self.params[key][img_], cv2.COLOR_BGR2GRAY )
        img_gauss      = cv2.GaussianBlur( img_gray, (5,5), 0 )
        img_canny      = cv2.Canny( img_gauss, threshold1=th1, threshold2=th2 )
        circles        = cv2.HoughCircles( img_canny, cv2.HOUGH_GRADIENT, minDist=minDist, \
                                           dp=dp, minRadius=minRadius, maxRadius=maxRadius )
        if ( circles is not None ):
            circles        = circles[0]
            nCircles       = circles.shape[0]
            for circle in circles:
                x, y, r    = int( circle[0] ), int( circle[1] ), int( circle[2] )
                img_show   = cv2.circle( img_rgb, (x, y), r, (255, 255, 0), 4 )
        else:
            img_show = np.copy( img_rgb )
        pE.set_data( img_show )
        canvas.draw()
        
    
        
    # ========================================================= #
    # ===  load__fileButton                                 === #
    # ========================================================= #
    def load__fileButton( self ):

        key  = "FileOpen01"

        # ------------------------------------------------- #
        # --- [1] get File path from Entry              --- #
        # ------------------------------------------------- #
        ekey = key + ".entry"
        path = ( self.widgets[ekey].get() )
        if ( not( os.path.exists( path ) ) ):
            print( "\n" + "[define__gui.py] Cannot find such a file... [ERROR] "   )
            print(        "[define__gui.py]  filename :: {}".format( path ) + "\n" )
            return()
        # ------------------------------------------------- #
        # --- [2] if the path is directory              --- #
        # ------------------------------------------------- #
        if ( os.path.isdir( path ) ):
            path = self.open__fileDialogBox( initDir=path )
        # ------------------------------------------------- #
        # --- [3] set path to the variable              --- #
        # ------------------------------------------------- #
        if ( os.path.isfile( path ) ):
            self.values [key].set( path )
            self.params ["opencv"] = [ path, None ]
            self.draw__opencvWindow()
        else:
            print( "\n" + "[define__gui.py] path is NOT file path... [ERROR] "   )
            print(        "[define__gui.py]  filename :: {}".format( path ) + "\n" )
        return()
    
            
    # ========================================================= #
    # ===  load__fileDialog                                 === #
    # ========================================================= #
    def load__fileDialog( self ):
        
        key  = "FileOpen01"

        # ------------------------------------------------- #
        # --- [1] open Dialog Box & set it in variable  --- #
        # ------------------------------------------------- #
        path = self.open__fileDialogBox()
        if ( len( path ) == 0 ):
            return
        self.values [key].set( path )
        self.params ["opencv"] = [ path, None ]
        self.draw__opencvWindow()
        return()
    
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    define__gui()








        # # ------------------------------------------------- #
        # # --- [1] Entry widgets                         --- #
        # # ------------------------------------------------- #
        # #  -- for multi line text input,                --  #
        # #  --    use tk.Text, instead                   --  #
        # # ------------------------------------------------- #
        # self.widgets["Entry01"] = ttk.Entry( self )

        # # ------------------------------------------------- #
        # # --- [2] Button widgets                        --- #
        # # ------------------------------------------------- #
        # self.functions["Button01"] = self.function
        # self.widgets  ["Button01"] = ttk.Button( self, text="update", \
        #                                          command=self.functions["Button01"] )
        
        # # ------------------------------------------------- #
        # # --- [3] Label widgets                         --- #
        # # ------------------------------------------------- #
        # #  -- for multi line message,                   --  #
        # #  --    use tk.Message, instead                --  #
        # # ------------------------------------------------- #
        # self.widgets["Label01"] = ttk.Label( self, text="Label", width=200 )

        # # ------------------------------------------------- #
        # # --- [4] Checkbutton widgets                   --- #
        # # ------------------------------------------------- #
        # self.values ["Checkbutton01"] = tk.BooleanVar()
        # self.widgets["Checkbutton01"] = ttk.Checkbutton( self, text="Checkbutton", \
        #                                                  variable=self.values["Checkbutton01"] )
        
        # # ------------------------------------------------- #
        # # --- [5] Radiobutton widgets                   --- #
        # # ------------------------------------------------- #
        # key   = "Radiobutton01"
        # items = { "A":"A", "B":"B", "C":"C" }
        # self.values [key]  = tk.StringVar()
        # self.params [key]  = items
        # for ik,item_key in enumerate( self.params[key].keys() ):
        #     wkey               = "{0}-{1}".format( key, item_key )
        #     text,value         =  item_key, self.params[key][item_key] 
        #     self.widgets[wkey] = ttk.Radiobutton( self, text=text, value=value,\
        #                                           variable=self.values[key] )

        # # ------------------------------------------------- #
        # # --- [6] Combobox widgets                      --- #
        # # ------------------------------------------------- #
        # self.values ["Combobox01"] = tk.StringVar()
        # self.params ["Combobox01"] = [ "type-A", "type-B", "type-C" ]
        # self.widgets["Combobox01"] = ttk.Combobox( self, textvariable=self.values["Combobox01"],\
        #                                            values=self.params["Combobox01"] )

        # # ------------------------------------------------- #
        # # --- [7] Scale widgets                         --- #
        # # ------------------------------------------------- #
        # self.values ["Scale01"] = tk.DoubleVar()
        # self.params ["Scale01"] = [ 0, 10 ]
        # self.widgets["Scale01"] = ttk.Scale( self, variable=self.values["Scale01"], \
        #                                      orient=tk.HORIZONTAL, length=200, \
        #                                      from_=self.params["Scale01"][0], \
        #                                      to_  =self.params["Scale01"][1], \
        #                                      command=self.draw__matplotlibWindow )
        
        # # ------------------------------------------------- #
        # # --- [6] Spinbox widgets                       --- #
        # # ------------------------------------------------- #
        # self.params ["Spinbox01"] = ["Type-A", "Type-B", "Type-C"]
        # self.widgets["Spinbox01"] = ttk.Spinbox( self, values=self.params["Spinbox01"] )
        # self.widgets["Spinbox02"] = ttk.Spinbox( self, values=self.params["Spinbox01"] )


        
        # # ------------------------------------------------- #
        # # --- [8] File Dialog Box Button                --- #
        # # ------------------------------------------------- #
        # self.widgets["FileDialog01"] = ttk.Button( self, text="Open File",\
        #                                            command=self.open__fileDialogBox )
        
        # # ------------------------------------------------- #
        # # --- [10] menu widgets                         --- #
        # # ------------------------------------------------- #
        # self.Menu_Entity     = tk.Menu( self.root )
        # self.Menus["menu01"] = tk.Menu( self.Menu_Entity, tearoff=False )
        # self.Menus["menu01"].add_command( label="command01", command=self.function )
        # self.Menus["menu01"].add_command( label="command02", command=self.function )
        # self.Menus["menu02"] = tk.Menu( self.Menu_Entity, tearoff=False )
        # self.Menus["menu02"].add_command( label="command01", command=self.function )
        # self.Menus["menu02"].add_command( label="command02", command=self.function )
        # self.Menu_Entity.add_cascade( label="menu01", menu=self.Menus["menu01"] )
        # self.Menu_Entity.add_cascade( label="menu02", menu=self.Menus["menu02"] )
        # self.root.config( menu=self.Menu_Entity )
        
