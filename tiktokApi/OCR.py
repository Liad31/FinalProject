
from matplotlib.pyplot import text
import requests

import json
import time
import cv2
import sys
import pickle
import pandas as pd
# Import required packages
import cv2
import sys
from moviepy.editor import *
import easyocr
reader = easyocr.Reader(['ar','en']) # this needs to run only once to load the model into memory
import openai
import os.path as  osp

def roundToN(x, base=1):
    return base * round(x/base)
def compareBoxes(b1,b2):
    if abs(b1[1]-b2[1])>10:
        return b1[1]-b2[1]
    else:
        return b1[0]-b2[0]
class BoxesComparator(object):
    def __init__(self, x):
        self.lst=x[0][0]
    def __lt__(self, other):
        if abs(self.lst[1]-other.lst[1])>10:
            return self.lst[1]<other.lst[1]
        else:
            return self.lst[0]>other.lst[0]
def text_from_video(path):
    def extract_middle_frame(path):
        # loading video gfg
        clip = VideoFileClip(path)


        # getting duration of the video
        duration = clip.duration

        # saving a frame at 1 second
        clip.save_frame("frame.png", int(duration/2))

        # showing clip

    extract_middle_frame(path)
    image_path="frame.png"
    img=cv2.imread(image_path)
    height=img.shape[0]
    img=img[int(height*0.1):-int(height*0.1),:]
    results = reader.readtext(img)
    final=[]
    results.sort(key=BoxesComparator)
    for bbox,text,conf in results:
        # print(f"text: {text}, conf: {conf}, bbox: {bbox}")
        if conf> 0.25:
            final.append(text)
    # final=final[1:]
    final=" ".join(final)
    final=' '.join(final.split())
    if not final or len(final)>150:
        return final
    response = openai.Completion.create(
      engine="davinci",
      prompt=f"Fix Spelling Mistakes\nOriginal:{final}\nStandard Arabic:",
      temperature=0,
      max_tokens=200,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["\n"]
    )
    aifinal=response['choices'][0]['text']
    if not aifinal:
        aifinal=final
    return aifinal.strip()

#import grequests
def create_download_txt(lis_sec_ids,path="async_list.txt"):
    # delete the previous downlaod
    os.system(f"rm {path}")
    for (sec,id) in lis_sec_ids:
        os.system(f'echo "https://www.tiktok.com/@{sec}/video/{id}" >> {path}')
def chunker_list(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
def ocr(videos,videosDir="/mnt/videos"):
    cur_time = time.time()
    cnt=0
    batch_size =batch_size
    passed_total = 0
    # get from the server a list of videos to download
    r = {"Vid":v for v in videos}
    rl = r.json()
    # print(rl)
    # take chunks of batch_size each time
    cnt_batch=0
    vids_to_download=[]
    for j in rl:
        secuid =j["Vid"]
        id = j["Vid"]
        vids_to_download.append((secuid,id))
    videoTexts=[]
    async_list = "async_list.txt"
    create_download_txt(vids_to_download,async_list)
    a=os.system(f'yt-dlp -a {async_list} -o "%(id)s.mp4" -R 10 --proxy frzgcmrj-rotate:rxpxcauy7pn0@p.webshare.io:80')
    for (secuid,id) in vids_to_download:
        path =f"{videosDir}/{id}.mp4"
        cur_path = f"./{id}.mp4"
        if not os.path.exists(f"{cur_path}"):
            # add to failed
            videoTexts.append({"Vid":id,"text":"ERROR2!!!!!"})
            # print("failed to download 15 vids")
            #continue
        os.system(f"mv {cur_path} {path}")
        while True:
            try:
                videoTexts.append({"Vid":id, "text": text_from_video(path)})
                break
            except OSError as e:
                with open("failed_vids",'a') as f:
                    f.write(f"{id}\n")
                videoTexts.append({"Vid":id, "text": ""})
                break
            except Exception as e:
                if not tokens:
                    print("no tokens")
                    return
                openai.api_key = tokens.pop()
        
        passed = time.time()-cur_time
        passed_total+=passed
            #print(f"Downloaded no videos in {passed} seconds")
        if cnt_batch!=0:
            print(f"Downloaded  and resized {cnt_batch} new vids in {passed:0.2f} secs, approx {passed/cnt_batch:0.2f}s per video")
        cur_time= time.time()
        # put an average of 50-100 vids
        if cnt >50:
            print(f"SUMMARY - Downloaded  and resized {cnt} vids in {passed_total:0.2f} secs, approx {passed_total/cnt:0.2f}s per video")
            # reset the counter
            cnt = 0
            passed_total=0
        requests.post(f'http://localhost:8001/api/database/markVideosDownloaded', json={"videos":videoTexts})
    print("finished the iterations!")
    return videoTexts
# text_from_video.counter=0
# import glob
# for i in glob.glob("*.mp4"):
#     text_from_video(i)
tokens=[]
# open file relative to package folder
this_dir, this_filename = os.path.split(__file__)
with open(osp.join(this_dir, "tokens.txt")) as f:
    for line in f:
        tokens.append(line.strip())
openai.api_key=tokens.pop()
ocr(iterations=1000,tokens=tokens)