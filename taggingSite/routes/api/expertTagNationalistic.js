let express = require("express");
let router = express.Router();
const mlTaggedVid = require("../../models/mlTaggedVid");
const Video = require("../../models/video");
const NodeCache = require("node-cache");
// TTL=30 mins
const recentlySent = new NodeCache({ stdTTL: 30 * 60 * 60, checkperiod: 0 });

router.get("/getVid", (req, res) => {
    for (key of recentlySent.keys()) {
        recentlySent.get(key)
    }
    let filter = {
        expertTag: null,
        _id: { $nin: recentlySent.keys() }
    }
    mlTaggedVid.findOne(filter, function (err, vid) {
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
    mlTaggedVid.findById(id, function (err, vid) {
        if (err) {
            console.log(err)
            return
        }
        
        console.log(vid)
        console.log(decision)
        vid.expertTag = decision;
        console.log(vid)
        vid.save()

        //update user
        let user = req.user;
        user.weekly_tags_left -= 1;
        user.save();
    })
    res.status(200).send();
})
module.exports = router;