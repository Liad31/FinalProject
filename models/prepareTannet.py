from sklearn.model_selection import train_test_split
if __package__ is None or __package__ == "":
    from imageUtils import extractFps
else:
    from .imageUtils import extractFps
import numpy as np
import cv2
import os
from tqdm import tqdm
def createIfNotExists(path):
    if not os.path.exists(path):
        os.mkdir(path)
def makeList(videos,tags,videosRoots):
    for id,tag in zip(videos,tags):
        # vid=id+".mp4"
        # if not os.path.exists(f"{vid_root}/{vid}"):
        #     print(vid)
            # continue
        # # save each frame seperately
        cont=False
        for videosRoot in videosRoots:
            if os.path.exists(f"{videosRoot}/{id}"):
                cont=True
        if cont:
            continue
        with open("vids2.txt","a") as f:
            f.write(f"{id} {tag}\n")
            # continue
def organize(videos,tags,annoFile,videosRoot,fps=10,vid_root="/mnt/videos"):
    # find last occurence of slash
    lastOcc=annoFile.rfind('/')
    # get the path to the videos
    annoRoot=annoFile[:lastOcc]
    createIfNotExists(annoRoot)
    createIfNotExists(videosRoot)
    i=0
    for id,tag in tqdm(zip(videos,tags)):
        i+=1
        vid=id+".mp4"
        if not os.path.exists(f"{vid_root}/{vid}"):
            with open("failed_vids.txt","a") as f:
                f.write(f"{vid}\n")
            # continue
        # # save each frame seperately
        if os.path.exists(f"{videosRoot}/{id}"):
            # with open("vids2.txt","a+") as f:
            #     f.write(f"{id}\n")
            continue
        extractFps(f"{vid_root}/{vid}",fps,videosRoot+'/'+id)
        # get number of files in dir
        onlyfiles = next(os.walk(videosRoot+'/'+id))[2] #dir is your directory path as string
        numFrames=len(onlyfiles)
        with open(annoFile,"a") as f:
            if(int(tag) in [0,1]):
                f.write(f"{id} {numFrames} {int(tag)}\n")
if "__main__"==__name__:
    root="/mnt/tannetFinalSite4/"
    createIfNotExists(root)
    data_root = root+'train'
    data_root_val = root+'val'
    data_root_test = root+"test"
    ann_file_train = root+'anno/train.txt'
    ann_file_val = root+'anno/val.txt'
    ann_file_test = root+'anno/test.txt'
    testVids=np.load('data.npy',allow_pickle=True)
    testVids= [i["Vid"] for i in testVids]
    tag=[0 for i in range(len(testVids))]
    organize(testVids,tag,ann_file_test,data_root_test)
# vidRoots=[data_root,data_root_val,data_root_test]
# vids=[]
# tags=[]
# with open("vids2.txt") as f:
#     for line in f:
#         vid,tag=line.split()
#         vids.append(vid)
#         tags.append(int(tag))
# organize(vids,tags,ann_file_test,data_root_test)
# vids=np.load("data.npy",allow_pickle=True)
# tag=np.load("tag.npy",allow_pickle=True)
# vids=[i["Vid"] for i in vids]
# organize(vids,tag,ann_file_train,data_root)

    # vids=np.load("data.npy",allow_pickle=True)
    # tag=np.load("tag.npy",allow_pickle=True)
    # vids=[i["Vid"] for i in vids]
    # organize(vids,tag,ann_file_train,data_root)


# vids=np.load("x_test.npy",allow_pickle=True)
# tag=np.load("y_test.npy",allow_pickle=True)
# vids=[i["Vid"] for i in vids]
# organize(vids,tag,ann_file_test,data_root_test)