from attr import has
if __package__ is None or __package__ == '':
    from scraper import scraper
else:
    from .scraper import scraper
import requests
import json
from datetime import datetime
def addToDB(output,yieldRes=False,locationFilter=True,ignore_location=False):
    usersWithLocation=output
    if locationFilter:
        usersWithLocation = [user for user in output if user["governorate"]]
    
    for i,user in enumerate(usersWithLocation):
        posts=user["posts"]
        postsDic=dict([(k["id"],j) for j,k in enumerate(posts)])
        reducedPosts=[posts[j] for j in postsDic.values()]
        usersWithLocation[i]["posts"]=reducedPosts

        
    for user in usersWithLocation:
        res = []
        videos = []
        for video in user["posts"]:
            utc_time = datetime.strptime(video["upload_date"], "%Y-%m-%dT%H:%M:%S")
            epoch_time = int(utc_time.timestamp())
            videos.append({"Vid": video["id"],
                           "text": video["description"],
                           "hashtags": video["hashtags"],
                           "musicId": video["music"]["id"],
                           "musicUrl": video["music"]["url"],
                           "stats": video['stats'],
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
        if user["governorate"] or ignore_location:
            requests.post("http://localhost:8001/api/database/postNewUsers",
                          data=json.dumps(x), headers=headers)
        if yieldRes:
            yield res
        
def addToDBNoYield(output,yieldRes=False,locationFilter=True,ignore_location=False):
    usersWithLocation=output
    if locationFilter:
        usersWithLocation = [user for user in output if user["governorate"]]

    for i,user in enumerate(usersWithLocation):
        posts=user["posts"]
        postsDic=dict([(k["id"],j) for j,k in enumerate(posts)])
        reducedPosts=[posts[j] for j in postsDic.values()]
        usersWithLocation[i]["posts"]=reducedPosts

        
    for user in usersWithLocation:
        res = []
        videos = []
        for video in user["posts"]:
            utc_time = datetime.strptime(video["upload_date"], "%Y-%m-%dT%H:%M:%S")
            epoch_time = int(utc_time.timestamp())
            videos.append({"Vid": video["id"],
                           "text": video["description"],
                           "hashtags": video["hashtags"],
                           "musicId": video["music"]["id"],
                           "musicUrl": video["music"]["url"],
                           "stats": video['stats'],
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
        if user["governorate"] or ignore_location:
            requests.post("http://localhost:8001/api/database/postNewUsers",
                          data=json.dumps(x), headers=headers)
if __name__ == "__main__":
    numPosts = 100000
    since = 0
    before = 0
    with open("hashtags.txt", "r") as file:
        hashtags = file.readlines()

    for hashtag in hashtags:
        if " " in hashtag:
            hashtags.append(hashtag.replace(" ", ""))
            hashtags.append(hashtag.replace(" ", "_"))
    hashtags=list(set(hashtags))
    output = scraper.scrap_hashtags(hashtags, numPosts, since, before,download=False)
    addToDBNoYield(output)