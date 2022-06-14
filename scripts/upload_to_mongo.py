import numpy as np
import  pymongo
from sklearn import metrics
from sklearn.metrics import accuracy_score
from tqdm import tqdm
def upload(ids, preds):
    myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production3?retryWrites=true&w=majority")
    db = myclient['production3']
    video_db = db['videos']
    # videos = list(video_db.find())
    # u = np.array(videos)[videos['score']>=0]
    # videos_id_list = [x['Vid'] for x in videos]
    for id,pred in tqdm(zip(ids,preds)):
        try:

            score = float(pred.replace('\n',''))
        except:
            print('id not found in the database')
            raise -1
        video_db.update_one({'Vid':id}, {"$set": {"score":score}}, upsert=False)

def calc_auc():
    pass

def random_scores_users():
    myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production3?retryWrites=true&w=majority")
    db = myclient['production3']
    users_db = db['tiktokusernationalistics']
    users = list(users_db.find())
    for user in users:
        user['nationalisticScore'] = np.random.rand()
        user['relevancyScore'] = np.random.rand()
        users_db.update_one({'userId': user['userId']}, {"$set": user}, upsert=False)

def calc_auc_amen():
    predictions = []
    tags = []
    # with open('../../Downloads/preds.txt', 'r') as f:
    #     preds = f.readlines()
    myclient = pymongo.MongoClient(
        "mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production3?retryWrites=true&w=majority")
    db = myclient['production3']
    real_db = db['mltaggedvids']
    tags_from_db = list(real_db.find())
    data = list(db['videos'].find())
    id = [str(x['_id']) for x in data]
    scores = [str(x['score']) for x in data]
    for tag in tags_from_db:
        vid = tag['vid']
        tag = tag['expertTag']
        if tag != None and tag == 1 or tag == 0:
            tags.append(tag)
            try:
                predictions.append(scores[id.index(str(vid))])
            except:
                print(1)
    good_idx = [i for i, e in enumerate(predictions) if e != '-1']
    tags = np.array(tags)[good_idx]
    predictions = np.array(predictions)[good_idx]
    predictions = [float(i) for i in predictions]
    tags = [float(i) for i in tags]
    fpr, tpr, thresholds = metrics.roc_curve(tags, predictions)
    print(len([1 for yhat, y in zip(predictions, tags) if yhat >= 0.5 and y == 1 or yhat < 0.3 and y == 0])/len(tags))
    print(metrics.auc(fpr, tpr))


if __name__ == "__main__":
    data = np.load('../models/data.npy', allow_pickle=True)
    # calc_auc_amen()
    with open('../preds5.txt', 'r') as f:
        preds = f.readlines()
    assert len(preds) == len(data)
    ids = [x['Vid'] for x in data]
    upload(ids, preds)



# if __name__ == "__main__":
#     random_scores_users()
