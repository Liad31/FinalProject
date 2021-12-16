from scraper import scraper
import requests
import json
from time import sleep
from datetime import datetime
numPosts = 1000
postsPerUser = 5
since = 0
before = 0
with open("hashtags.txt", "r") as file:
    hashtags = file.read().split(',')


# hashtags= ["food","arab"]
output = scraper.scrap_hashtags(hashtags, numPosts, since, before)
usersWithLocation = [user for user in output if user["governorate"]]
# usersWithLocation=output
# scrap some unnecessary info but do it in one command
# excessVideos=scraper.scrap_users([user["username"] for user in usersWithLocation],postsPerUser-1,since,before)
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
                       "date":epoch_time
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
