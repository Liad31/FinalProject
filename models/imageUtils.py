import os
import cv2
import numpy as np
# tmpDir='/tmp/videos'
def extractFps(video,fps,dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    os.system(f'ffmpeg -i {video} -vf fps={fps} {dir}/img_%05d.jpg')
    #remove dir
    # os.system(f'rm -r {tmpDir}')
    # return np.array(data)

def extractNumFrames(video,numFramesExtract):
    # determine video length in seconds
    videoLength=os.popen(f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video}').read()
    videoLength=float(videoLength)
    return extractFps(video,numFramesExtract/videoLength)