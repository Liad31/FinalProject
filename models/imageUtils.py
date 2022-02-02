import os
import cv2
import numpy as np
videosDir='videos'
tmpDir='tmp'
def extractFps(video,fps):
    if not os.path.exists(tmpDir):
        os.mkdir(tmpDir)
    os.system(f'ffmpeg -i {videosDir}/{video}.mp4 -vf fps={fps} {tmpDir}/%d.jpg')
    data=[]
    for frame in os.listdir(tmpDir):
        data.append(cv2.imread(tmpDir+'/'+frame))
    #remove dir
    os.system(f'rm -rf {tmpDir}')
    return np.array(data)

def extractNumFrames(video,numFramesExtract):
    # determine video length in seconds
    videoLength=os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {videosDir}/{video}.mp4').read()
    videoLength=float(videoLength)
    return extractFps(video,numFramesExtract/videoLength)