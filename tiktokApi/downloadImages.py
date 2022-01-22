
from scraper import scraper
import requests
import json
import os
from moviepy.editor import *
numPosts = 2000
since = 0
before = 0
folder="#standwithisrael"
hashtag= "standwithisrael"
framesFolder="frames"

def extract_middle_frame(path,name,framesFolder):

    # loading video gfg
    clip = VideoFileClip(path)


    # getting duration of the video
    duration = clip.duration

    # saving a frame at 1 second
    clip.save_frame(f"./{framesFolder}/{name}.png", int(duration/2))

headers={"Content-Type": "application/json"}
for file in os.listdir(folder):
    fileName=file.split(".")[0]
    path=os.path.join(folder,file)
    try:
        extract_middle_frame(path,fileName,framesFolder)
        requests.post("http://localhost:8001/api/database/postNewImage", data=json.dumps({"id":fileName}), headers=headers)  
    except Exception as e:
        os.remove(path)
        print(path)
        print(e)