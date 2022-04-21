import numpy as np
import  pymongo
from scipy.stats import sem

def calc(num):
    x =  (num-mean)/std
    return (x-mini)/(maxi-mini)
myclient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production3?retryWrites=true&w=majority")
#
# db = myclient['production3']
# users_db = db['tiktokusernationalistics']
#
# likes = []
# followers = []
#
# users = users_db.find()
# for user in users:
#     likes.append(user['userStats']['likes_count'])
#     followers.append(user['userStats']['followers_count'])
#
# up_likes =  np.mean(likes) + 2* sem(likes)
# up_followers =  np.mean(likes) + 2* sem(likes)
# up_followers = np.mean(followers)+3*sem(followers)
# likes = np.array(likes)
# followers = np.array(followers)
# np.save('likes.npy',likes)
# np.save('followers.npy',followers)

likes = np.load('likes.npy',allow_pickle=True)
followers = np.load('followers.npy',allow_pickle=True)
likes = np.log(likes)
followers = np.log(followers)
followers[followers<0]=0
likes[likes<0]=0
likes = (likes - np.min(likes)) / (np.max(likes) - np.min(likes))
followers = (followers - np.min(followers)) / (np.max(followers) - np.min(followers))
print(1)

