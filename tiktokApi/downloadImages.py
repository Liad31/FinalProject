
from scraper import scraper
import requests
import json
import os
from moviepy.editor import *
# numPosts = 1
since = 0
before = 0
folder="#israel"
hashtags= ["israel"]
framesFolder="frames"
# usersWithLocation = [user for user in output if user["governorate"]]
# for i,user in enumerate(usersWithLocation):
#     usersWithLocation[i]["posts"]=list(filter(lambda x: isLegal(x["upload_date"]),user["posts"]))
# usersWithLocation=list(filter(lambda x: len(x["posts"])>0,usersWithLocation)) 
# os.mkdir(framesFolder)
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