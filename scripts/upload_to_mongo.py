import numpy as np
import  pymongo

def upload(ids, preds):
    myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production3?retryWrites=true&w=majority")
    db = myclient['production3']
    video_db = db['videos']
    videos = list(video_db.find())
    u = np.array(videos)[videos['score']>=0]
    videos_id_list = [x['Vid'] for x in videos]
    for id in ids:
        try:
            i = videos_id_list.index(id)
            post = videos[i]
            post['score'] = float(preds[i].replace('\n',''))
        except:
            print('id not found in the database')
            raise -1
        video_db.update_one({'Vid':id}, {"$set": post}, upsert=False)

def calc_auc():
    pass

data = np.load('../../Downloads/data.npy', allow_pickle=True)
with open('../../Downloads/preds.txt', 'r') as f:
    preds = f.readlines()
ids = [x['Vid'] for x in data]
upload(ids, preds)
