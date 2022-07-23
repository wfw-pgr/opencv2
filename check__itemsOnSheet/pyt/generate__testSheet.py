import os, sys
import cv2
import numpy as np

# ========================================================= #
# ===  generate__testSheet.py                           === #
# ========================================================= #

def generate__testSheet( figsize=(1200,900), marker_size=50 ):

    x_, y_, rc_, f_ = 0, 1, 2, 3

    # ------------------------------------------------- #
    # --- [1] generate new figure                   --- #
    # ------------------------------------------------- #
    image = np.ones( (figsize[y_],figsize[x_] ), dtype=np.uint8 ) * 255
    
    # ------------------------------------------------- #
    # --- [2] generate AR marker                    --- #
    # ------------------------------------------------- #
    aruco         = cv2.aruco
    markers_dict  = aruco.getPredefinedDictionary( aruco.DICT_4X4_50  )
    markers_imgs  = [ aruco.drawMarker( markers_dict, ARid, marker_size ) for ARid in range(4) ]

    # ------------------------------------------------- #
    # --- [3] put AR marker on image                --- #
    # ------------------------------------------------- #
    l_,u_,r_,b_   = 0, 1, 2, 3
    lurb_margin   = [ 20, 20, 20, 20 ]
    right_, bot_  = figsize[x_] - marker_size, figsize[y_] - marker_size
    lurb_pos      = [ +        lurb_margin[l_], +      lurb_margin[u_], \
                      right_ - lurb_margin[u_], bot_ - lurb_margin[b_] ]
    bbs           = [ [ lurb_pos[l_], lurb_pos[u_] ], \
                      [ lurb_pos[r_], lurb_pos[u_] ], \
                      [ lurb_pos[r_], lurb_pos[b_] ], \
                      [ lurb_pos[l_], lurb_pos[b_] ]  ]
    bbs           = np.array( bbs, dtype=np.int32 )
    ms            = np.repeat( np.array( [marker_size,marker_size],dtype=np.int32 )[None,:], 4, axis=0 )
    bbs_          = bbs + ms
    bbs           = np.concatenate( [bbs,bbs_], axis=1 )
    
    for ik, bb in enumerate( bbs ):
        image[ bb[1]:bb[3], bb[0]:bb[2] ] = markers_imgs[ik]

    xavg  = ( bbs[:,0] + bbs[:,2] ) * 0.5 
    yavg  = ( bbs[:,1] + bbs[:,3] ) * 0.5
    xyavg = np.concatenate( [xavg[:,None],yavg[:,None]], axis=1 )
    import nkUtilities.save__pointFile as spf
    ids       = np.arange( xyavg.shape[0] ) + 1
    Data      = np.concatenate( [ids[:,None],xyavg], axis=1 )
    outFile   = "dat/armarker_pos.dat"
    spf.save__pointFile( outFile=outFile, Data=Data )
    
    # ------------------------------------------------- #
    # --- [4] draw rectangular outline              --- #
    # ------------------------------------------------- #
    thickness     = 4
    white_margin  = 10
    black_color   = (0,0,0)
    pt1, pt2      = np.copy( bbs[0,0:2]-white_margin ), np.copy( bbs[2,2:4]+white_margin )
    image         = cv2.rectangle( image, pt1, pt2, black_color, \
                                   thickness=thickness, lineType=cv2.LINE_8 )

    # ------------------------------------------------- #
    # --- [5] draw holes                            --- #
    # ------------------------------------------------- #
    import nkUtilities.load__pointFile as lpf
    inpFile  = "dat/holeData.dat"
    holeData = lpf.load__pointFile( inpFile=inpFile, returnType="point" )
    holeData = holeData.astype( np.int32 )

    flag__deviation = True
    max_dev         = 3
    if ( flag__deviation ):
        deviation = np.random.normal( loc=0.0, scale=max_dev, size=(holeData.shape[0],2))
        holeData[:,x_:y_+1]  = holeData[:,x_:y_+1] + deviation
    
    linetype = 4
    for ik, coo in enumerate( holeData ):
        image = cv2.circle( image, (coo[x_], coo[y_]), coo[rc_], black_color, linetype )

    # ------------------------------------------------- #
    # --- [6] fill circles                          --- #
    # ------------------------------------------------- #
    fillhole = holeData[ np.where( holeData[:,f_] == 1.0  ) ]
    for ik, coo in enumerate( fillhole ):
        image = cv2.circle( image, (coo[x_], coo[y_]), coo[rc_], black_color, \
                            thickness=-1 )
    print( np.min( holeData[:,x_] ), np.max( holeData[:,x_] ) )
    print( np.min( holeData[:,y_] ), np.max( holeData[:,y_] ) )

    # ------------------------------------------------- #
    # --- [7] save in a file                        --- #
    # ------------------------------------------------- #
    outFile = "jpg/testSheet.jpg"
    cv2.imwrite( outFile, image )
    
    
# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    generate__testSheet()
