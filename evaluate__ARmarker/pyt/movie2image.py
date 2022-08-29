import nkOpenCV.save__movieFrames as smf

frame_to_use = "first"
inpFile      = "mov/sample_original.mov"
outFile      = "jpg/sample"
smf.save__movieFrames( inpFile=inpFile, outFile=outFile, frame_to_use=frame_to_use )

# original image AR marker size = [ 52 x 52 ]
