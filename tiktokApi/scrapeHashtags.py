from scraper import scraper
import requests
import json
from time import sleep
from datetime import datetime
numPosts = 5000
postsPerUser = 5
since = 0
before = 0
legalTimestamps=[(1617235200,1619827200),(1497398400,1497484800)]
def isLegal(date):
    utc_time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    epoch_time = int(utc_time.timestamp())
    for legalTimestamp in legalTimestamps:
        if legalTimestamp[0]<epoch_time<legalTimestamp[1]:
            if legalTimestamp[0]==1497484800:
                print("bloop")
            return True
    return False
with open("hashtags.txt", "r") as file:
    hashtags = file.readlines()


# hashtags= ["food","arab"]
output = scraper.scrap_hashtags(hashtags, numPosts, since, before)
usersWithLocation = [user for user in output if user["governorate"]]
# usersWithLocation=output
# scrap some unnecessary info but do it in one command
# excessVideos=scraper.scrap_users([user["username"] for user in usersWithLocation],postsPerUser-1,since,before)
# print(len([vid for user in usersWithLocation for vid in user["posts"] if isLegal(vid["upload_date"])]))
for i,user in enumerate(usersWithLocation):
    usersWithLocation[i]["posts"]=list(filter(lambda x: isLegal(x["upload_date"]),user["posts"]))
    if not usersWithLocation[i]["posts"]:
        usersWithLocation.pop(i)

    
for user in usersWithLocation:
    res = []
    videos = []
    # numVideosNeeded=postsPerUser-len(videos)
    # scrapedVideos=[scrapped["posts"] for scrapped in excessVideos if user["id"]==scrapped["id"]][0]
    for video in user["posts"]:
        utc_time = datetime.strptime(video["upload_date"], "%Y-%m-%dT%H:%M:%S")
        epoch_time = int(utc_time.timestamp())
        videos.append({"Vid": video["id"],
                       "text": video["description"],
                       "hashtags": video["hashtags"],
                       "musicId": video["music"]["id"],
                       "musicUrl": video["music"]["url"],
                       "date": epoch_time
                       })
    res.append({
        "id": user["id"],
        "userName": user["username"],
        "governorate": user["governorate"],
        "videos": videos,
        "bio": user["bio"],
        "userStats": user["stats"]
    })
    x = {"users": res}
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}
    requests.post("http://localhost:8001/api/database/postNewUsers",
                  data=json.dumps(x), headers=headers)
