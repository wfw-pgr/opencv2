import os, sys, cv2, copy
import numpy as np


# ========================================================= #
# ===  generate__testSheet.py                           === #
# ========================================================= #

def generate__testSheet():

    x_, y_, rc_, f_ = 0, 1, 2, 3
    black_color     = (0,0,0)
    markerType      = cv2.aruco.DICT_4X4_50

    # ------------------------------------------------- #
    # --- [0] load constants                        --- #
    # ------------------------------------------------- #
    import nkUtilities.load__constants as lcn
    cnsFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=cnsFile )
    
    # ------------------------------------------------- #
    # --- [1] generate new figure                   --- #
    # ------------------------------------------------- #
    image = np.ones( ( const["figsize"][y_], const["figsize"][x_] ), dtype=np.uint8 ) * 255
    
    # ------------------------------------------------- #
    # --- [2] prepare AR marker                     --- #
    # ------------------------------------------------- #
    aruco         = cv2.aruco
    markers_dict  = aruco.getPredefinedDictionary( markerType )
    markers_imgs  = [ aruco.drawMarker( markers_dict, ARid, const["marker.size"] ) for ARid in range(4) ]

    # ------------------------------------------------- #
    # --- [3] put AR marker on image                --- #
    # ------------------------------------------------- #
    iSize     = ( const["figsize"][x_], const["figsize"][y_] )
    locations = [ const["marker.pos.{:02}".format( ik+1 )] for ik in range( len(markers_imgs) ) ]
    cent      = int( const["marker.size"]*0.5 )
    import nkOpenCV.overlay__image as ovl
    for ik,img in enumerate(markers_imgs):
        location = copy.copy( locations[ik] )
        image    = ovl.overlay__image( base=image, overlay=img, location=location, \
                                       centering=True )
        
    # ------------------------------------------------- #
    # --- [4] draw / fill holes                     --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    holeData = lpf.load__pointFile( inpFile=const["holeFile"], returnType="point" )
    holeData = holeData.astype( np.int32 )
    fillhole = holeData[ np.where( holeData[:,f_] == 1.0  ) ]
    linetype = 4
    for ik,coo in enumerate( holeData ):
        image = cv2.circle( image, (coo[x_], coo[y_]), coo[rc_], black_color, linetype     )
    for ik, coo in enumerate( fillhole ):
        image = cv2.circle( image, (coo[x_], coo[y_]), coo[rc_], black_color, thickness=-1 )

    # ------------------------------------------------- #
    # --- [5] save in a file                        --- #
    # ------------------------------------------------- #
    cv2.imwrite( const["outFile"], image )

    # ------------------------------------------------- #
    # --- [6] save AR marker position in a file     --- #
    # ------------------------------------------------- #
    locations = np.array( locations )
    import nkUtilities.save__pointFile as spf
    outFile   = "dat/ARmarker_pos.dat"
    spf.save__pointFile( outFile=outFile, Data=locations )

    
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    generate__testSheet()
