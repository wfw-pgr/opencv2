import os, sys, inspect
import cv2
import numpy       as np
import tkinter     as tk
import tkinter.ttk as ttk
import matplotlib.pyplot                 as plt
import matplotlib.backends.backend_tkagg as btk
import nkGUI.gui__base as gui


# ========================================================= #
# ===  define_gui                                       === #
# ========================================================= #

class practice__gui:

    # ========================================================= #
    # ===  constructor                                      === #
    # ========================================================= #
    def __init__( title="gui", width=None, height=None ):

        # ------------------------------------------------- #
        # --- [1] arguments                             --- #
        # ------------------------------------------------- #
        if ( width  is None ):
            width  = 800
            print( "[practice__gui.py] default {0:12} : {1}  is used.".format( "width" , width  ) )
        if ( height is None ):
            height = 800
            print( "[practice__gui.py] default {0:12} : {1}  is used.".format( "height", height ) )
        
        # ------------------------------------------------- #
        # --- [2] define gui application                --- #
        # ------------------------------------------------- #
        frame = tk.Tk()
        frame.title   ( title )
        frame.geometry( "{0}x{1}".format( width, height ) )
        base  = gui__edit( frame, width=width, height=height )
        frame.mainloop()


# ========================================================= #
# ===  gui__edit                                        === #
# ========================================================= #

class gui__edit( gui.gui__base ):

    # ========================================================= #
    # ===  initialize of the class                          === #
    # ========================================================= #
    def __init__( self, root=None, width=400, height=800 ):
        super().__init__( root, width=width, height=height )

    # ========================================================= #
    # ===  Parameter Setting part                           === #
    # ========================================================= #
        
    # ========================================================= #
    # ===  set function name                                === #
    # ========================================================= #
    def set__functions( self ):

        # ------------------------------------------------- #
        # ---   store associated function name          --- #
        # ------------------------------------------------- #
        self.functions["Adjust.Canny01"]    = lambda: self.update__opencvWindow_Canny( key="opencv.Canny" )
        self.functions["Adjust.Canny02"]    = lambda: self.update__opencvWindow_Canny( key="opencv.Canny" )
        self.functions["Adjust.Canny03"]    = lambda: self.update__opencvWindow_Canny( key="opencv.Canny" )
        self.functions["Adjust.Hough01"]    = lambda: self.update__opencvWindow_Hough( key="opencv.Hough" )
        self.functions["Adjust.Hough02"]    = lambda: self.update__opencvWindow_Hough( key="opencv.Hough" )
        self.functions["Adjust.Hough03"]    = lambda: self.update__opencvWindow_Hough( key="opencv.Hough" )
        self.functions["Adjust.Hough04"]    = lambda: self.update__opencvWindow_Hough( key="opencv.Hough" )
        self.functions["Adjust.Hough05"]    = lambda: self.update__opencvWindow_Hough( key="opencv.Hough" )
        self.functions["FileOpen01.button"] = self.load__fileButton
        self.functions["FileOpen01.dialog"] = self.load__fileDialog
        self.functions["FileOpen01"]        = lambda: self.set__opencvWindows( key_win1="opencv.Canny", key_win2="opencv.Hough" )
        self.functions["opencv.Canny"]      = lambda: self.draw__opencvWindow( key="opencv.Canny" )
        self.functions["opencv.Hough"]      = lambda: self.draw__opencvWindow( key="opencv.Hough" )

        return()


    # ========================================================= #
    # ===  set Parameters                                   === #
    # ========================================================= #
    def set__params( self ):

        # ------------------------------------------------- #
        # ---   store parameters to be used             --- #
        # ------------------------------------------------- #
        #   < params > [ min, max, init, increment ]   #
        self.params["Adjust.Canny01"]   = [ 0, 255,  90,   1 ]  # th1
        self.params["Adjust.Canny02"]   = [ 0, 255, 110,   1 ]  # th2
        self.params["Adjust.Canny03"]   = [ 0,  49,   5,   2 ]  # th2
        self.params["Adjust.Hough05"]   = [ 0, 300.0, 100.0, 1.0]  # param2
        # self.params["Adjust.Hough05"]   = [ 0, 1.0, 0.9, 0.01]  # param2
        self.params["Adjust.Hough01"]   = [ 0,   5, 1.5, 0.1 ]  # dp  : resolution
        self.params["Adjust.Hough02"]   = [ 0, 1.0, 0.1, 0.01]  # minimum Distance :: normalized 
        self.params["Adjust.Hough03"]   = [ 0, 1.0, 0.1, 0.01]  # minimum Radius   :: normalized
        self.params["Adjust.Hough04"]   = [ 0, 1.0, 0.3, 0.01]  # maximum Distance :: normalized
        #   < params > None :: initialize
        self.params["opencv.Canny"] = None
        self.params["opencv.Hough"] = None

        #   < params > target params key to store file name & Data #
        self.params["FileOpen01"]  = "opencv.Canny"
        
        return()


    # ========================================================= #
    # ===  set label name                                   === #
    # ========================================================= #
    def set__labels( self ):

        # ------------------------------------------------- #
        # ---   store lable for each widget             --- #
        # ------------------------------------------------- #
        self.labels["Adjust.Canny01"]     = "threshold1"
        self.labels["Adjust.Canny02"]     = "threshold2"
        self.labels["Adjust.Canny03"]     = "GaussFilter"
        self.labels["Adjust.Hough05"]     = "param2"
        self.labels["Adjust.Hough01"]     = "dp"
        self.labels["Adjust.Hough02"]     = "min_Distance"
        self.labels["Adjust.Hough03"]     = "min_Radius"
        self.labels["Adjust.Hough04"]     = "max_Radius"
        self.labels["FileOpen01.button"]  = "Load"
        self.labels["FileOpen01.dialog"]  = "Open File"

        return()


    # ========================================================= #
    # ===  set position of the widgets                      === #
    # ========================================================= #
    def set__positions( self ):

        # posits (list) :: [ relx, rely, relwidth, relheight, anchor ]
        
        # ------------------------------------------------- #
        # ---     specify position directory            --- #
        # ------------------------------------------------- #
        self.posits ["FileOpen01.entry"]       = [  0.05, 0.03, 0.70, None ]
        self.posits ["FileOpen01.button"]      = [  0.77, 0.03, 0.18, None ]
        self.posits ["FileOpen01.dialog"]      = [  0.05, 0.07, 0.90, None ]
        self.posits ["Adjust.Canny01.label"]   = [  0.28, 0.15, 0.40, 0.08, "center"  ]
        self.posits ["Adjust.Canny01.scale"]   = [  0.10, 0.15, 0.25, None ]
        self.posits ["Adjust.Canny01.spinb"]   = [  0.36, 0.15, 0.10, None ]
        self.posits ["Adjust.Canny02.label"]   = [  0.73, 0.15, 0.40, 0.08, "center" ]
        self.posits ["Adjust.Canny02.scale"]   = [  0.55, 0.15, 0.25, None ]
        self.posits ["Adjust.Canny02.spinb"]   = [  0.81, 0.15, 0.10, None ]
        self.posits ["Adjust.Canny03.label"]   = [  0.28, 0.25, 0.40, 0.08, "center" ]
        self.posits ["Adjust.Canny03.scale"]   = [  0.10, 0.25, 0.25, None ]
        self.posits ["Adjust.Canny03.spinb"]   = [  0.36, 0.25, 0.10, None ]
        self.posits ["Adjust.Hough05.label"]   = [  0.73, 0.25, 0.40, 0.08, "center"  ]
        self.posits ["Adjust.Hough05.scale"]   = [  0.55, 0.25, 0.25, None ]
        self.posits ["Adjust.Hough05.spinb"]   = [  0.81, 0.25, 0.10, None ]
        self.posits ["Adjust.Hough01.label"]   = [  0.28, 0.35, 0.40, 0.08, "center"  ]
        self.posits ["Adjust.Hough01.scale"]   = [  0.10, 0.35, 0.25, None ]
        self.posits ["Adjust.Hough01.spinb"]   = [  0.36, 0.35, 0.10, None ]
        self.posits ["Adjust.Hough02.label"]   = [  0.73, 0.35, 0.40, 0.08, "center" ]
        self.posits ["Adjust.Hough02.scale"]   = [  0.55, 0.35, 0.25, None ]
        self.posits ["Adjust.Hough02.spinb"]   = [  0.81, 0.35, 0.10, None ]
        self.posits ["Adjust.Hough03.label"]   = [  0.28, 0.45, 0.40, 0.08, "center"  ]
        self.posits ["Adjust.Hough03.scale"]   = [  0.10, 0.45, 0.25, None ]
        self.posits ["Adjust.Hough03.spinb"]   = [  0.36, 0.45, 0.10, None ]
        self.posits ["Adjust.Hough04.label"]   = [  0.73, 0.45, 0.40, 0.08, "center" ]
        self.posits ["Adjust.Hough04.scale"]   = [  0.55, 0.45, 0.25, None ]
        self.posits ["Adjust.Hough04.spinb"]   = [  0.81, 0.45, 0.10, None ]
        self.posits ["opencv.Canny"]           = [  0.08, 0.52, 0.40, 0.45 ]
        self.posits ["opencv.Hough"]           = [  0.52, 0.52, 0.40, 0.45 ]
        return()


    # ========================================================= #
    # ===  create widgets                                   === #
    # ========================================================= #
    def create__widgets( self ):

        self.widgets__FileOpen    ( key="FileOpen01" )
        self.widgets__adjustParams( key="Adjust.Canny01"  )
        self.widgets__adjustParams( key="Adjust.Canny02"  )
        self.widgets__adjustParams( key="Adjust.Canny03"  )
        self.widgets__adjustParams( key="Adjust.Hough05"  )
        self.widgets__adjustParams( key="Adjust.Hough01"  )
        self.widgets__adjustParams( key="Adjust.Hough02"  )
        self.widgets__adjustParams( key="Adjust.Hough03"  )
        self.widgets__adjustParams( key="Adjust.Hough04"  )
        self.window__matplotlib   ( key="opencv.Canny" )
        self.window__matplotlib   ( key="opencv.Hough" )

        
        
    # ========================================================= # ================= #
    # ===  user definition functions                        === # 
    # ========================================================= # ================= #

    # ========================================================= #
    # ===  update__opencv_Canny                             === #
    # ========================================================= #
    def update__opencvWindow_Canny( self, event=None, key=None ):

        name_, img_    = 0, 1
        if ( key is None ): sys.exit( "[update__opencvWindow] key == ???" )
        
        # ------------------------------------------------- #
        # --- [1] modify opencv images                  --- #
        # ------------------------------------------------- #
        _,ax,pE,canvas = self.values[key]
        th1            =   int( float( self.values["Adjust.Canny01"].get() ) )
        th2            =   int( float( self.values["Adjust.Canny02"].get() ) )
        iGauss         =   int(      ( self.values["Adjust.Canny03"].get() ) )

        # ------------------------------------------------- #
        # --- [2] canny                                 --- #
        # ------------------------------------------------- #

        
        img_rgb        = cv2.cvtColor( self.params[key][img_], cv2.COLOR_BGR2RGB  )
        img_gray       = cv2.cvtColor( self.params[key][img_], cv2.COLOR_BGR2GRAY )
        img_gauss      = cv2.GaussianBlur( img_gray, (iGauss,iGauss), 0 )

        # med_val = np.median(img_gauss)
        # sigma   = 0.33  # 0.33
        # min_val = int(max(0, (1.0 - sigma) * med_val))
        # max_val = int(max(255, (1.0 + sigma) * med_val))
        # th1,th2 = min_val, max_val

        img_canny      = cv2.Canny( img_gauss, threshold1=th1, threshold2=th2 )
        img_show       = img_canny
        
        pE.set_data( img_canny )
        canvas.draw()
        
        
    # ========================================================= #
    # ===  update__opencv_Hough                             === #
    # ========================================================= #
    def update__opencvWindow_Hough( self, event=None, key=None ):

        name_, img_    = 0, 1
        if ( key is None ): sys.exit( "[update__opencvWindow] key == ???" )
        refLength      = np.min( self.params[key][img_].shape[0:2] )
        
        # ------------------------------------------------- #
        # --- [1] modify opencv images                  --- #
        # ------------------------------------------------- #
        _,ax,pE,canvas = self.values[key]
        th1            =   int( float( self.values["Adjust.Canny01"].get() )  )
        th2            =   int( float( self.values["Adjust.Canny02"].get() )  )
        iGauss         =   int(      ( self.values["Adjust.Canny03"].get() )  )
        param2         =        float( self.values["Adjust.Hough05"].get() )
        dp             =        float( self.values["Adjust.Hough01"].get() )
        minDist        =   int( float( self.values["Adjust.Hough02" ].get() ) * refLength )
        minRadius      =   int( float( self.values["Adjust.Hough03" ].get() ) * refLength )
        maxRadius      =   int( float( self.values["Adjust.Hough04" ].get() ) * refLength )

        # ------------------------------------------------- #
        # --- [2] canny                                 --- #
        # ------------------------------------------------- #
        img_rgb        = cv2.cvtColor( self.params[key][img_], cv2.COLOR_BGR2RGB  )
        img_gray       = cv2.cvtColor( self.params[key][img_], cv2.COLOR_BGR2GRAY )
        img_gauss      = cv2.GaussianBlur( img_gray, (iGauss,iGauss), 0 )
        img_canny      = cv2.Canny( img_gauss, threshold1=th1, threshold2=th2 )
        circles        = cv2.HoughCircles( img_canny, cv2.HOUGH_GRADIENT, minDist=minDist,
                                           param1=max(th1,th2), param2=param2, \
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
    # ===  set__opencvWindows when load file                === #
    # ========================================================= #
    def set__opencvWindows( self, event=None, key_win1=None, key_win2=None ):

        if ( key_win1 is None ): sys.exit( "[update__opencvWindow] key_win1 == ???" )
        if ( key_win2 is None ): sys.exit( "[update__opencvWindow] key_win2 == ???" )

        path   = ( self.values["FileOpen01"] ).get()
        self.params[key_win2] = [ path, None ]

        self.draw__opencvWindow( key="opencv.Canny" )
        self.draw__opencvWindow( key="opencv.Hough" )
        self.update__opencvWindow_Canny( key=key_win1 )
        self.update__opencvWindow_Hough( key=key_win2 )
        return()

    
    # ========================================================= #
    # ===  draw__matplotlib                                 === #
    # ========================================================= #
    def draw__matplotlibWindow( self, event=None, key=None ):

        if ( key is None ): sys.exit( "[draw__matplotlibWindow] key == ???" )
        
        params_key    = "Adjust.Hough01.scale"
        # ------------------------------------------------- #
        # --- [2] plot area                             --- #
        # ------------------------------------------------- #
        ax,pE,canvas  = ( self.values[key] )[1:]
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
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    ret = practice__gui()

