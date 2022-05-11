from  models.final_model import final_model
from models.hashtags_models import  get_hash_score
from  models.text_models import model as nlp
from  models.text_models import dataprep
from  models.audio import get_train_sounds
from models.text_models.config import Config
from models.final_model.final_model import postsModel
from models.text_models.trail_nlp import embed_text2
from models.hashtags_models.roy import predict
from models.prepareTannet import organize, createIfNotExists
# from flask import Flask, request,jsonify
import os
import tempfile
import torch
import  numpy as np
# import requests
import  json
from tiktokApi.scraper import scraper
from tiktokApi.OCR import ocr
from tiktokApi.scrapeHashtags import addToDB
import requests
import pymongo
from flask import Flask, request,jsonify
import datetime
nationalistic_sounds = np.load('models/nationalistic_songs.npy', allow_pickle=True)
mongoClient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")
model = torch.load('models/final_model/final_model', map_location='cpu')
app= Flask(__name__)
def idFromUrl(url):
    return url.split("/")[-1]
@app.route('/predict', methods=['GET'])
def videoScores():
    urls=request.args.get('urls')
    urls=json.loads(urls)
    res=score_from_url(urls)
    return jsonify(res)
@app.route("/getVideos", methods=["GET"])
def getVideos():
    urls=request.args.get('urls')
    urls=json.loads(urls)
    db = mongoClient["production3"]
    usersDB = db["users"]
    ids= [idFromUrl(i) for i in urls]
    res = usersDB.find({"Vid": {"$in": ids}})
    for i in res:
        del i["_id"]
    return jsonify(list(res))
@app.route("/getUsers", methods=["GET"])
def getUsers():
    users=request.args.get('users')
    users=json.loads(users)
    db = mongoClient["production3"]
    usersDB = db["tiktokusernationalistics"]
    res= usersDB.find({"userName": {"$in": users}})
    return jsonify(list(res))
@app.route("/videosFromLast", methods=['GET'])
def videosFromLast():
    db= mongoClient["production3"]
    videosDB= db["videos"]
    if 'hours' in request.args: 
        hours=request.args.get('hours')
        hours=int(hours)
        time= datetime.datetime.now()-datetime.timedelta(hours=hours)
        timeInEpoch = int(time.timestamp())
        filter= {"dateInt": {"$gt": timeInEpoch}}
    else:
        filter={}
    # count results
    res=videosDB.aggregate([
    {
        '$addFields': {
            'dateInt': {
                '$toInt': '$date'
            }
        }
    }, {
        '$match': filter}])
    res = list(res)
    for i in res:
        del i["_id"]
        if "user" in i:
            del i["user"]
    return jsonify(res)
@app.route("/usersCount", methods=['GET'])
def usersCount():
    db= mongoClient["production3"]
    usersDB= db["tiktokusernationalistics"]
    res=usersDB.find()
    res = len(list(res))
    return jsonify(res)
@app.route("/videosCount", methods=['GET'])
def videosCount():
    db= mongoClient["production3"]
    videosDB= db["videos"]
    res=videosDB.find()
    res = len(list(res))
    return jsonify(res)

@app.route('/mostNationalistic', methods=['GET'])
def getNationalistic():
    username = request.args.get('user')
    n = request.args.get('n')
    db = mongoClient["production3"]
    usersDB= db["tiktokusernationalistics"]
    videoDB= db["videos"]
    user=usersDB.find_one({"userName":username})
    # populate videos
    # get the top scored videos
    vidIds=user["videos"]
    # turn object id to objects
    vidsCursor=videoDB.find({"_id":{"$in":vidIds}})
    vids= [i for i in vidsCursor]
    vids.sort(key=lambda x:x["score"],reverse=True)
    vids=vids[:int(n)]
    # remove _id field
    for vid in vids:
        del vid["_id"]
    return jsonify(vids)
@app.route('/topUsers', methods=['GET'])
def topUsers():
    n = request.args.get('n')
    sort= request.args.get('sort')
    db = mongoClient["production3"]
    usersDB= db["tiktokusernationalistics"]
    users=usersDB.find().sort(sort,pymongo.DESCENDING).limit(int(n))
    users=[i for i in users]
    for user in users:
        del user["_id"]
        del user["videos"]
    return jsonify(users)
@app.route("/topVideos", methods=['GET'])
def topVideos():
    n = request.args.get('n')
    sort= request.args.get('sort')
    db = mongoClient["production3"]
    videosDB= db["videos"]
    videos = videosDB.find().sort(sort,pymongo.DESCENDING).limit(int(n))
    videos=[i for i in videos]
    for i in videos:
        del i["_id"]
        if "user" in i:
            del i["user"]
    return jsonify(videos)
@app.route("/is1500InHaraza",methods=['GET'])
def yes():
    return jsonify("yes")
def updateNationalisticScores():
    pass
def apply_video_model(vids,vidsRoot):
    with tempfile.TemporaryDirectory() as root:
        dataRootTest=root+"/test"
        annoFileTest=root+"/anno/test.txt"
        organize(vids,[0 for _ in vids],annoFileTest,dataRootTest,vid_root=vidsRoot)
        confFile="./models/videoModel/mmaction2/configs/recognition/tanet/conf.py"
        with open(confFile) as f:
            lines=f.readlines()
        lines[5]=f'root="{root}/"\n'
        with open(confFile,"w") as f:
            f.writelines(lines)
        prefix="models/videoModel/mmaction2/"
        a=os.system(f"python3 {prefix}tools/test.py {confFile} {prefix}/work_dirs/tanet/epoch_12.pth --out results.json")
        with open("results.json") as f:
            results=json.load(f)
        return results
    
def score_from_url(urls):
    with tempfile.TemporaryDirectory() as videoRoot:
        userMeta=scraper.scrap_postsUrl(urls)
        if len(userMeta)==0:
            return []
        data=[]
        for user in addToDB(userMeta,yieldRes=True,locationFilter=False):
            data.extend(user[0]["videos"])
        ids=[i["Vid"] for i in data]
        videoText=ocr(ids,videoRoot)
        for video,text in zip(data,videoText):
            video["videoText"]=text["text"]
        # find the path of the video in directory
        return predictSamples(ids,data,videoRoot)
def download_user_vids(users,num_posts=20):
    videoRoot="/mnt/videos"
    userMeta=scraper.scrap_users(users,num_posts=num_posts)
    data=[]
    for user in addToDB(userMeta,yieldRes=True,locationFilter=False,ignore_location=True):
        data.extend(user[0]["videos"])
    ids=[i["Vid"] for i in data]
    videoText=ocr(ids,videoRoot)
    for video,text in zip(data,videoText):
        video["videoText"]=text["text"]
    # find the path of the video in directory
    return data
def score_for_users(users,num_posts=20):
    with tempfile.TemporaryDirectory() as videoRoot:
        userMeta=scraper.scrap_users(users,num_posts=num_posts)
        data=[]
        for user in addToDB(userMeta,yieldRes=True,locationFilter=False,ignore_location=True):
            data.extend(user[0]["videos"])
        ids=[i["Vid"] for i in data]
        videoText=ocr(ids,videoRoot)
        for video,text in zip(data,videoText):
            video["videoText"]=text["text"]
        # find the path of the video in directory
        return predictSamples(ids,data,videoRoot)
def get_hashtag_score(data):
    res=predict(data,np.zeros(1))
    res=[i["hash_score"] for i in data]
    res=torch.tensor(res)
    return res
def get_sound_score(data):
    return [i["musicId"] in nationalistic_sounds for i in data]
def predictSamples(ids,dataArray,root):
    videoVecs=apply_video_model(ids,root)
    res=[]
    for data,videoVec in zip(dataArray,videoVecs):
        id=data["Vid"]
        data=[data]
        x={}
        x["video_embeded"]=torch.tensor(videoVec)
        x["sound"]=get_sound_score(data)
        x["sound"]=torch.tensor(x["sound"])
        x["hashtags_score"]=get_hashtag_score(data)
        embed_text2(data,np.zeros(1))
        x["text"]=[d['text'] for d in data]
        x["text_embeded"]=[d['text_embeded'] for d in data]
        x["text_embeded"]= x["text_embeded"][0]
        res.append({"Vid":id,"result": float(final_model.get_predict(model,sample=x))})
    return res
def predictAll():
    videoResultsFile="models/videoModel/mmaction2/finalVecs.json"
    dataFile="data.npy"
    batchSize=1
    with open(videoResultsFile) as f:
        videoVecs=json.load(f)
    data=np.load(dataFile,allow_pickle=True)
    # make data and vids in the same order
    # apply models
    with open("/mnt/tannetIdk/anno/test.txt") as f:
        lines=f.readlines()
        allowedVids=[line.strip() for line in lines]
        allowedVids=[lines.split()[0] for lines in allowedVids]
    allowedVids=set(allowedVids)
    preds=[]
    from tqdm import tqdm
    for i in tqdm(range(0,100 ,batchSize)):
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
    with open("predsCopy.txt","w+") as f:
        f.writelines([str(p)+'\n' for p in preds])
def update_video_scores(scores):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    requests.post("http://localhost:8001/api/database/updateScores",
                  data=json.dumps({"scores":scores}), headers=headers)
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
    # db = mongoClient['production3']
    # users_db = db['tiktokusernationalistics']
    # users= db['tiktokusernationalistics']
    # videos= db['videos']
    # for user in users.find():
    #     download_user_vids([user['userId']],num_posts=20)
