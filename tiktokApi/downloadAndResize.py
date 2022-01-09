
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

    # extract_middle_frame(path)
    image_path="frame.png"
    img=cv2.imread(image_path)
    img=img[80:-80,:]
    results = reader.readtext(img)
    final=[]
    results.sort(key=BoxesComparator)
    for bbox,text,conf in results:
        # print(f"text: {text}, conf: {conf}, bbox: {bbox}")
        if conf> 0.4:
            final.append(text)
    # final=final[1:]
    final=" ".join(final)
    openai.api_key = "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"
    response = openai.Completion.create(
      engine="davinci",
      prompt=f"Correct Mistakes In The Original Text\nOriginal:{final}\nStandard Arabic:",
      temperature=0,
      max_tokens=200,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=0.0,
      stop=["\n"]
    )
    return response['choices'][0]['text']


#import grequests
def create_download_txt(lis_sec_ids,path="async_list.txt"):
    # delete the previous downlaod
    os.system(f"rm {path}")
    for (sec,id) in lis_sec_ids:
        os.system(f'echo "https://www.tiktok.com/@{sec}/video/{id}" >> {path}')
def chunker_list(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def async_download_vids_parallel(batch_size =10,iterations=500):
    # request the videos from server
    num_videos = 20#2
    cur_time = time.time()
    cnt=0
    cnt_failed=0
    batch_size =batch_size
    num_threads=10
    passed_total = 0
    
    id_success=[]
    i=0
    while i<iterations:
        id_failed=[]
        # get from the server a list of videos to download
        r = requests.get(f'http://localhost:8001/api/database/getVideos?num={num_videos}')
        rl = r.json()
        if len(rl) ==0:
            print("finished downloading!")
            break
        # print(rl)
        # take chunks of batch_size each time
        for chunk in chunker_list(rl,batch_size):
            cnt_batch=0
            vids_to_download=[]
            for j in chunk:
                secuid =j["Vid"]
                id = j["Vid"]
                vids_to_download.append((secuid,id))
            videoTexts=[]
            async_list = "async_list.txt"
            create_download_txt(vids_to_download,async_list)
            os.system(f"tiktok-scraper from-file {async_list} {num_threads}  --proxy-file ../proxies.txt -d")
            downloaded_paths = []
            for (secuid,id) in vids_to_download:
                # check in current folder
                cur_path = f"./{id}.mp4"
                # or get_file_size(cur_path)==0
                if not os.path.exists(f"{cur_path}"):
                    # add to failed
                    cnt_failed+=1
                    id_failed.append(id)
                    if cnt_failed%15==0:
                        print(id)
                        exit()
                    # print("failed to download 15 vids")
                    #continue
                else:
                    # move the file
                    if not os.path.exists('videos'):
                        os.system(f"mkdir videos")
                    path =f"./videos/{id}.mp4"
                    new_path = path[:-4]+"_r.mp4"
                    os.system(f"mv {cur_path} {path}")
                    videoTexts.append({"Vid":id, "text": text_from_video(path)})
                    downloaded_paths.append((path,new_path))
                    cnt_batch+=1
                    cnt+=1
            # resize the vids
            resize_videos_parallel(downloaded_paths)
            # override the old vids
            for (path,new_path) in downloaded_paths:
                os.system(f"mv {new_path} {path}")
                secuid_v = path[2:].split("/")[0]
                id_v = path[2:].split("/")[1][:-4]
                id_success.append(id_v)
            # tell the server it changed
            
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
            requests.post(f'http://localhost:8001/api/database/addVideoText', json={"videos":videoTexts})
        
        i+=1
    print("finished the iterations!")
import ffmpeg
def resize_videos_parallel(paths,scale_percent = 100,size_factor=3,new_path="output3.mp4"):
    #,res=(540,960)
    #around of 112k pixels resolution should be ok
    # preprae for each vid its command and then run parallel on it
    # delete last commands
    command_path = "command_resize.txt"
    os.system(f"rm {command_path}")
    for (path,new_path) in paths:
        # percent of original size
        #get reoslution 
        scale_percent = 100 /2 #100 / size_factor
        res = os.popen(f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{path}"').read()
        res = (int(res.split("x")[0]), int(res.split("x")[1]))
        width = int(res[0] * scale_percent / 100)
        height = int(res[1] * scale_percent / 100)
        dim = (width, height)
        # get bit rate
        probe= ffmpeg.probe(path)['streams']
        vid_bit_rate=int(probe[0]['bit_rate'])
        #-map 0:a -b:a {new_music_rate}k {new_path[:-6]}.m4a 
        new_vid_rate=int(vid_bit_rate/size_factor /1000)
        
        # do a minimum of 200 kbytes
        new_vid_rate = max(200,new_vid_rate)

        # max of 900 kbytes
        new_vid_rate = min(900,new_vid_rate)

        # add a check
        """
        # check for minimum 35k for music
        new_music_rate=max(int(music_bit_rate/1000 * 0.5),35)
        if len(probe) <2:
            print("missing music in {path}, skipping it")
            continue
        music_bit_rate=int(probe[1]['bit_rate'])
        """
        #-b:a {new_music_rate}k
        # we cant ovveride the exisint file so we create one and then we move it
        #ffmpeg -i vid.avi -map 0:a audio.wav -map 0:v onlyvideo.avi
        # add to file

        #</dev/null > /dev/null 2>&1
        command = f"ffmpeg -i {path} -s {width}x{height} -b:v {new_vid_rate}k -map 0:v {new_path}"
        os.system(f"echo {command} >> {command_path}")
    # run the parallel on it- which basically runs a lot of instructions a the same time
    os.system(f"parallel -a {command_path}")
    #print(os.popen("parallel -a command_resize.txt").read())
    return
def get_failed_vids():
    import os 
    from collections import defaultdict
    if os.path.exists("failed_vids"):
        loaded_dict=pickle.load(open("failed_vids",'rb'))
        cnt = sum([len(val) for val in loaded_dict.values()])
        print(f"loaded failed vids from cache, {cnt} videos were previously failed")
        return loaded_dict
    print("created a new failed cache")
    loaded_dict=defaultdict(list)
    pickle.dump(loaded_dict, open("failed_vids",'wb'))
    return loaded_dict
def chunker(seq, size):
    return (seq[pos:pos + size].reset_index(drop=True) for pos in range(0, len(seq), size))
def cleanup():
    os.system("rm cache_vids")
    os.system("rm failed_vids")
    os.system("rm async_list.txt")
    os.system("rm command_resize.txt")

def create_csv(cache_vids):
    data = []
    for videos in cache_vids.values():
        for vid in videos[0]:
            data.append(vid[:-4])
    # initialize list of lists
    
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns = ['id'])
    print(df)
    # convert to df 
    # save as csv drop index
    df.to_csv("../downloaded_vids.csv",index=False)

def count_videos():
    names=list(os.walk(os.getcwd()))[0][1]
    #print(names)
    #for each entry, add the video name
    dict_vids=defaultdict(list)
    cnt=0
    for entry,name in zip(list(os.walk(os.getcwd()))[1:],names):
        # ignore secret checkpoint
        if name != '.ipynb_checkpoints' :
            # count only .mp4 videos, not music
            vids =[entry for  entry in entry[2] if entry.endswith('.mp4')]
            cnt+= len(vids)
    print(f"found a total of {cnt} videos")
# text_from_video.counter=0
# import glob
# for i in glob.glob("*.mp4"):
#     text_from_video(i)
# async_download_vids_parallel()
print(text_from_video("a"))