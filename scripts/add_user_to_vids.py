import pandas as pd
import numpy as np
import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")

db = myclient['production3']
users_db = db['tiktokusernationalistics']
videos = db['videos']


users = users_db.find()
for idx, user in enumerate(users):
    for vid_id in user['videos']:
        vid = videos.find_one({'_id': vid_id})
        if vid is not None:
            if "user" not in vid.keys():
                vid["user"] = user['_id']
                videos.replace_one({"_id": vid["_id"]}, vid)
print("done!")
print(f'{dups_num}/{users.count()}')
