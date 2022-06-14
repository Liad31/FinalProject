import pandas as pd
import numpy as np
import pymongo
from bson.objectid import ObjectId
from  tqdm import tqdm
myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")\

db = myclient['production3']
users = db['tiktokusernationalistics']
videos =  db['videos']
tags = db['nationalistictags']
# tagged_uesrs = users.find({"inBatch":True})
# for user in tagged_uesrs:
#     if len(user['tags']):
#         tagged.append( user)
# tagged= list(tagged_uesrs)
videos= videos.find({"downloaded":True,"score":-1})
videos = list(videos)
data = []
vids = []
nationalistic_sounds = []
for video in tqdm(videos):
    if video['videoText'] != 'ERROR!!!!!':
        data.append(video)
        vids.append(video['Vid'])
data = np.array(data)
vids = np.array(vids)
nationalistic_sounds = np.array(nationalistic_sounds)
np.save('data', data)
np.save('vids', vids)
np.save('nationalistic_songs', nationalistic_sounds)
### for the nationalistic_songs run also  get_nat_songs.py

print("done!")
