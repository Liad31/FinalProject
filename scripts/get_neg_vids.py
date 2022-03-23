import pymongo


myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")

db = myclient['production2']
users_db = db['tiktokusernationalistics']
videos = db['videos']
tags = db['nationalistictags']
neg_vids = db['negvids']


users = users_db.find()
for user in users:
    videos = user['videos']
    if len(user['tags']) > 0:
        tag = tags.find_one(user['tags'][0])
        if tag:
            for idx, vid_tag in enumerate(tag['videoTag']):
                if not vid_tag['decision']:
                    if idx < len(videos):
                        tagged_video = {'vid': videos[idx], 'expertTag': None}
                        neg_vids.insert_one(tagged_video)

