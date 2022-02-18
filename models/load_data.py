import pandas as pd
import numpy as np
import pymongo
from bson.objectid import ObjectId
from  tqdm import tqdm
myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")\

db = myclient['production2']
users = db['tiktokusernationalistics']
videos =  db['videos']
tags = db['nationalistictags']
tagged = []

tagged = []
tagged_uesrs = users.find({},{"tags": 1 , "videos":1})
for user in tagged_uesrs:
    if len(user['tags']):
        tagged.append( user)

data = []
tag = []
vids = []
for user in tqdm(tagged):
    user_tag = tags.find_one({'_id':  ObjectId(user['tags'][0])})
    if user_tag:
        for x in range(len(user['videos'])):
                video = videos.find_one({'_id': ObjectId(user['videos'][x])})
                if video['videoText'] != 'ERROR2!!!!!':
                    data.append(video)
                    vids.append(video['Vid'])
                    try:
                        tag.append(user_tag['videoTag'][x]['decision'])
                    except:
                        data.pop(-1)
                        vids.pop(-1)
    else:
        videos_prod1 = myclient['production1']['videos']
        tags_prod1 = myclient['production1']['nationalistictags']
        user_tag = tags_prod1.find_one({'_id': ObjectId(user['tags'][0])})
        for x in range(len(user['videos'])):
            video = videos_prod1.find_one({'_id': ObjectId(user['videos'][x])})
            if video and ('videoText' not in video or video['videoText'] != 'ERROR2!!!!!'):
                data.append(video)
                vids.append(video['Vid'])
                tag.append(user_tag['videoTag'][x]['decision'])
data = np.array(data)
tag = np.array(tag)
vids = np.array(vids)
np.save('data', data)
np.save('tag', tag)
np.save('vids', vids)


print("done!")