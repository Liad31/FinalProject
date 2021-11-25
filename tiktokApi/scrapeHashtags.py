import scraper
numPosts=10
postsPerUser=5
hashtags=['أريحا']
output=scraper.scrap_hashtags(hashtags,numPosts)
usersWithLocation=[user for user in output if user["governorate"]]
# scrap some unnecessary info but do it in one command
excessVideos=scraper.scrap_users([user["username"] for user in usersWithLocation],numPosts-1)
for user in usersWithLocation:
    videos=[]
    numVideosNeeded=postsPerUser-len(videos)
    scrapedVideos=[scrapped["posts"] for scrapped in excessVideos if user["id"]==scrapped["id"]][0]
    for video in user["posts"]+scrapedVideos[:numVideosNeeded]:
        videos+={"Vid":video["id"],
                "text":video["name"],
                "hashtags": video["hashtags"],
                "musicId": video["music"]["id"],
                "musicUrl": video["music"]["url"],
                }
    res={
        "id": user["id"],
        "governorate": user["governorate"],
        "videos": [video["id"] for video in user["posts"]],
        "bio": user["bio"],
        "userStats": user["stats"],
    }
    
