from  models.final_model import final_model
from  models.final_model.dataset import  postsDataset
from models.hashtags_models import  get_hash_score
from  models.text_models import model as nlp
from  models.text_models import dataprep
from  models.audio import get_train_sounds
from models.text_models.config import Config
from models.final_model.final_model import postsModel
from models.text_models.trail_nlp import embed_text2
from models.hashtags_models.roy import predict
from models.prepareTannet import organize, createIfNotExists
from flask import Flask, request,jsonify
import os
import tempfile
import torch
import  numpy as np
import requests
import  json
app = Flask(__name__)
model = torch.load('models/final_model/final_model', map_location='cpu')
nationalistic_sounds = np.load('models/nationalistic_songs.npy', allow_pickle=True)
# nationalistic_sounds = get_train_sounds.get_train_sounds(x_train, nationalistic_sounds) # important to do!!!! x_train is data in data format

def apply_video_model(vids,vidsRoot):
    with tempfile.TemporaryDirectory() as root:
        createIfNotExists(root)
        dataRootTest=root+"/test"
        annoFileTest=root+"/anno/test.txt"
        organize(vids,[0 for _ in vids],annoFileTest,dataRootTest,vid_root=vidsRoot)
        confFile="models/videoModel/mmaction2/configs/recognition/tanet/myConf.py"
        with open(confFile) as f:
            lines=f.readlines()
        lines[6]=f'root="{root}"\n'
        with open(confFile,"w") as f:
            f.writelines(lines)
        prefix="models/videoModel/mmaction2/"
        a=os.system(f"python3 {prefix}tools/test.py {prefix}configs/recognition/tanet/myConf.py {prefix}tanet/epoch_12.pth --out results.json")
        with open("results.json") as f:
            results=json.load(f)
        return results
    
def score_from_url():
    #implement!!!!!!
    return requests.post(request.url_root + 'get_final_score', json={
    "text":"abc. abc",
    "hashtags":["#abc", "#def"],
    "sound": 123,
    "video": [[1,2,3],[4,5,6]]
    })
def get_hash_score(data):
    res=predict(data,np.zeros(1))
    res=[i["hash_score"] for i in data]
    res=torch.tensor(res)
    return res
def get_sound_score(data):
    return [i["musicId"] in nationalistic_sounds for i in data]
def predictSample(videoPath,data,root):
    videoVec=apply_video_model([videoPath],root)
    x={}
    x["video_embeded"]=torch.tensor(videoVec)
    x["sound"]=get_sound_score(data)
    x["sound"]=torch.tensor(x["sound"])
    x["hashtags_score"]=get_hash_score(data)
    x["text"]=[d['text'] for d in data]
    x["text_embeded"]=[d['text_embeded'] for d in data]
    x["text_embeded"]= x["text_embeded"][0]
    res=final_model.get_predict(model,sample=x)
    return res
def predictAll():
    videoResultsFile="models/videoModel/mmaction2/finalVecs.json"
    dataFile="x_test.npy"
    batchSize=1
    with open(videoResultsFile) as f:
        videoVecs=json.load(f)
    data=np.load(dataFile,allow_pickle=True)
    # make data and vids in the same order
    # apply models
    preds=[]
    from tqdm import tqdm
    for i in tqdm(range(0,len(videoVecs),batchSize)):
        x={}
        x["video_embeded"]=torch.tensor(videoVecs[i:i+batchSize])
        dataBatch=data[i:i+batchSize]
        x["hashtags_score"]=predict(dataBatch,np.zeros(batchSize))
        # make tensor
        x["hashtags_score"]=[i["hash_score"] for i in dataBatch]
        x["hashtags_score"]=torch.tensor(x["hashtags_score"])
        x["sound"]=[i["musicId"] in nationalistic_sounds for i in dataBatch]
        x["sound"]= torch.tensor(x["sound"])
        embed_text2(dataBatch,np.zeros(batchSize))
        x["text"]=[d['text'] for d in dataBatch]
        x["text_embeded"]=[d['text_embeded'] for d in dataBatch]
        x["text_embeded"]= x["text_embeded"][0]
        res=final_model.get_predict(model,sample=x)
        preds.extend([float(i) for i in res])
    with open("preds.txt","w+") as f:
        f.writelines([str(p)+'\n' for p in preds])
if __name__ == "__main__":
    predictAll()