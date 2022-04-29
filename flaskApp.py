from flask import Flask, request,jsonify
import json
from predictUtils import score_from_url
import pymongo
app= Flask(__name__)
@app.route('/predict', methods=['GET'])
def videoScores():
    urls=request.args.get('urls')
    urls=json.loads(urls)
    res=score_from_url(urls)
    return jsonify(res)
@app.route('/mostNationalistic', methods=['GET'])
def getNationalistic():
    username = request.args.get('user')
    n = request.args.get('n')
    mongoClient = pymongo.MongoClient("mongodb+srv://ourProject:EMGwk59xADuSIIkv@cluster0.lhfaj.mongodb.net/production2?retryWrites=true&w=majority")
    db = mongoClient["production3"]
    usersDB= db["tiktokusernationalistics"]
    videoDB= db["videos"]
    user=usersDB.find_one({"userName":username})
    # populate videos
    # get the top scored videos
    vidIds=user["videos"]
    # turn object id to objects
    vidsCursor=videoDB.find({"_id":{"$in":vidIds}})
    vids= [i for i in vidsCursor]
    vids.sort(key=lambda x:x["score"],reverse=True)
    vids=vids[:int(n)]
    # remove _id field
    for vid in vids:
        del vid["_id"]
    return jsonify(vids)
if __name__ == '__main__':
    # listen to all interfaces
    app.run(host='0.0.0.0', port=8080)