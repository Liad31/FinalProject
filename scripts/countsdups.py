import pandas as pd
import numpy as np
import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")

db = myclient['production2']
users_db = db['tiktokusernationalistics']
videos = db['videos']

dups_num = 0
users = users_db.find()
for idx, user in enumerate(users):
    vids = []
    for vid_id in user['videos']:
        vid = videos.find_one({'_id': vid_id})
        if vid is not None:
            vids.append(vid['Vid'])
    a_set = set(vids)
    if len(vids) != len(a_set):
        dups_num += 1
        print(f'{idx}: {user}')
        print(f'{dups_num}/{idx}')
print("done!")
print(f'{dups_num}/{users.count()}')
