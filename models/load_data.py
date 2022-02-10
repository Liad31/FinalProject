import pandas as pd
import numpy as np
import pymongo
from bson.objectid import ObjectId

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
for user in tagged:
    user_tag = tags.find_one({'_id':  ObjectId(user['tags'][0])})
    if user_tag:
        for x in range(len(user_tag['videoTag'])):
            video = videos.find_one({'_id': ObjectId(user['videos'][x])})
            if video['videoText'] != 'ERROR!!!!!':
                data.append(video)
                tag.append(user_tag['videoTag'][x]['decision'])
    # else:
    #     videos_prod1 = myclient['production1']['videos']
    #     tags_prod1 = myclient['production1']['nationalistictags']
    #     user_tag = tags_prod1.find_one({'_id': ObjectId(user['tags'][0])})
    #     for x in range(len(user['videos'])):
    #         video = videos_prod1.find_one({'_id': ObjectId(user['videos'][x])})
    #         if video and ('videoText' not in video or video['videoText'] != 'ERROR2!!!!!'):
    #             data.append(video)
    #             tag.append(user_tag['videoTag'][x]['decision'])
data = np.array(data)
tag = np.array(tag)
np.save('data', data)
np.save('tag', tag)



