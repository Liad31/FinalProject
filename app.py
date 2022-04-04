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

@app.route("/get_text_vector", methods=['POST'])
def get_text_vector():
    request_json = request.json
    data = [request_json['data']]
    embed_text2(data, [0])
    return jsonify(vector=list(data[0]['text_embeded']), is_text=data[0]['text'])

@app.route("/get_video_vector", methods=['POST'])
def get_video_vector():
    request_json = request.json
    video = np.array(request_json['video'])
    # implement!!!!
    return jsonify(vector=[0.6])
def apply_video_model(vids,vidsRoot):
    with tempfile.TemporaryDirectory() as root:
        createIfNotExists(root)
        dataRootTest=root+"/test"
        annoFileTest=root+"/anno/test.txt"
        organize(vids,[0 for _ in vids],annoFileTest,dataRootTest,vidsRoot=vidsRoot)
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
@app.route("/get_hashtags_score", methods=['POST'])
def get_hashtags_score():
    request_json = request.json
    data = [request_json['data']]
    predict(data, [0])
    return jsonify(
        score=list(data[0]['hash_score'])
    )
@app.route("/get_sound_score", methods=['POST'])
def get_sound_score():
    request_json = request.json
    sound = request_json['sound']
    res = 0
    if sound in nationalistic_sounds:
        res = 1
    return jsonify(
        score=[res]
    )
@app.route("/get_final_score", methods=['POST'])
def final_score():
    request_json =request.json
    root_url = request.url_root
    x = {}

    is_text = 0
    if 'text' in request_json:
        is_text = 1
        text_embeded = (requests.post(root_url + 'get_text_vector', json={"data": request_json})).json()['vector'] # todo: fix this, you get is_text as well!
        x['text_embeded'] = torch.tensor(text_embeded)
    else:
        x['text_embeded'] = torch.tensor(np.random.rand(128))

    video_embeded = (requests.post(root_url + 'get_video_vector', json={"video": request_json['video']})).json()['vector']
    x['video_embeded'] = torch.tensor(video_embeded)
    sound_score = (requests.post(root_url + 'get_sound_score', json={"sound":  request_json['sound']})).json()['score']
    x['sound'] = torch.tensor(sound_score)
    x['text'] = torch.tensor([is_text])
    hashtags_score = (requests.post(root_url + 'get_hashtags_score', json={"data":  request_json})).json()['score']
    x['hashtags_score'] = torch.tensor(hashtags_score)
    return str(final_model.get_predict(model, sample=x)[0])

@app.route("/get_final_score", methods=['POST'])
def score_from_url():
    #implement!!!!!!
    return requests.post(request.url_root + 'get_final_score', json={
    "text":"abc. abc",
    "hashtags":["#abc", "#def"],
    "sound": 123,
    "video": [[1,2,3],[4,5,6]]
    })
def predictAll():
    videoResultsFile="models/videoModel/mmaction2/trainVecs.json"
    dataFile="models/data.npy"
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
        x["text_embeded"]= torch.tensor(x["text_embeded"])
        res=final_model.get_predict(model,sample=x)
        preds.extend(res)
if __name__ == "__main__":
    predictAll()