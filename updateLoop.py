from tiktokApi.scraper import scraper
from tiktokApi.scraper import scraper
from tiktokApi.scrapeHashtags import addToDB
import pymongo
import time
mongoClient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")
def fetch_user_vids(users,num_posts=20):
    userMeta=scraper.scrap_users(users,num_posts=num_posts)
    for user in addToDB(userMeta,yieldRes=True,locationFilter=False,ignore_location=True):
        pass
db = mongoClient['production3']
users_db = db['tiktokusernationalistics']
users= db['tiktokusernationalistics']
videos= db['videos']
while True:
    u = users.find()
    u=list(u)
    from tqdm import tqdm
    u= tqdm(u)
    for user in u:
        fetch_user_vids([user['userName']],num_posts=20)
        # sleep for 6 hours
    time.sleep(21600)