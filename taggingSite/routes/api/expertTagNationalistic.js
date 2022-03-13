let express = require("express");
let router = express.Router();
const User = require("../../models/user")
const Tag = require("../../models/nationalisticTag")
const NegVid = require("../../models/negVid");
const Stats = require("../../models/nationalisticTaggingStat");
const Video = require("../../models/video");
const NodeCache = require("node-cache");
const { ObjectId, ObjectID } = require("bson");
const featureList = require("../../params/params").FEATURE_LIST
const MAX_VIDEOS_PER_TAG = require("../../params/params").MAX_VIDEOS_PER_TAG
const FeatureCounter = require("../../models/featureCounter")
// TTL=30 mins
const recentlySent = new NodeCache({ stdTTL: 30 * 60 * 60, checkperiod: 0 });

router.get("/getNegVid", (req, res) => {
    for (key of recentlySent.keys()) {
        recentlySent.get(key)
    }
    let filter = {
        expertTag: null,
        _id: { $nin: recentlySent.keys() }
    }
    NegVid.findOne(filter, function (err, vid) {
        if (err) {
            console.log(err)
            return
        }
        if (!vid) {
            // console.log("no user found")
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify(null))
        }
        else {
            Video.findById(vid.vid, function (err, video) {
                if (err) {
                    console.log(err)
                    return
                }
                if (!video) {
                    // console.log("no user found")
                    res.setHeader('Content-Type', 'application/json');
                    res.end(JSON.stringify(null))
                } else {
                    recentlySent.set(vid._id.toString(), 1)
                    res.setHeader('Content-Type', 'application/json');
                    res.end(JSON.stringify({ vidId: video.Vid, objId: vid._id }))
                }
            });
        }
    })
})

router.post("/markError", (req, res) => {
    let userID = req.body.id;
    console.log(userID + "marked as error");
    TiktokUser.findOne({ userId: userID }, function (err, user) {
        if (err) {
            console.log(err)
            return
        }
        user.error = 1;
        user.save();
    })
    res.status(200).send();
})

router.post("/tag", (req, res) => {
    let id = req.body.id
    let decision = req.body.tag
    NegVid.findById(id, function (err, negvid) {
        if (err) {
            console.log(err)
            return
        }
        
        console.log(negvid)
        console.log(decision)
        negvid.expertTag = decision;
        console.log(negvid)
        negvid.save()

        //update user
        let user = req.user;
        user.weekly_tags_left -= 1;
        user.save();
    })
    res.status(200).send();
})
module.exports = router;