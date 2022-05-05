import pymongo
from bson.objectid import ObjectId
import pymongo
import numpy as np
if __name__ == '__main__':
    # vids  = np.load('vids.npy', allow_pickle=True)
    # u, c = np.unique(vids, return_counts=True)
    # tags = np.load('tag.npy', allow_pickle=True)
    # dup = u[c>1]
    # for d in dup:
    #     t=[]
    #     for k in range(len(vids)):
    #         if vids[k] == d:
    #             t.append(tags[k])
    #     t1,t2 =np.unique(np.array(t),return_counts=True)
    #     print(t2)
    # print(vids)

    myclient = pymongo.MongoClient(
        "mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production3?retryWrites=true&w=majority")
    db = myclient['production3']
    users = db['tiktokusernationalistics']
    videos = db['videos']
    tags = db['nationalistictags']

    videos_objects = []
    all_videos = []
    cursor = users.find({})
    for document in cursor:
        videos_objects += document['videos']
    for d in range(len(videos_objects)):
        videos_objects[d] = str(videos_objects[d])
    cursor = videos.find({})
    for document in cursor:
        all_videos.append(str(document['_id']))

    ghost_vids = []
    for vid in all_videos:
        if vid not in videos_objects:
            print(vid)
            ghost_vids.append(vid)
    np.save('ghost_vids.npy', ghost_vids)
    # print(ghost_vids)


