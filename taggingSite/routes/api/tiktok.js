var express = require("express");
var router = express.Router();
const User = require("../../models/user")
const Tag = require("../../models/tag")
const TiktokUser = require("../../models/tiktokUser");
const Value = require("../../models/value.js");
const NodeCache = require("node-cache");
// TTL=30 mins
const recentlySent = new NodeCache({ stdTTL: 1 });// TODO:change back to 30*60*60 min!!!!!!!!!!!!!!!!!!!

router.post("/submitTag", (req, res) => {
    let params = req.body
})
router.get("/getUser", (req, res) => {
    let perms = req.user.Permissions
    console.log(perms)
    recentlySent.flushAll()
    let filter = {
        "tags.0": { $exists: false },
        userId: { $nin: recentlySent.keys() }
    }
    let options = {}
    filter.error = 0; // users marked in error won't bt given to tag
    // a regular user can't tag expert posts
    if (perms == 0) {
        filter.expertNeeded = 0
    }
    //an expert needs to see expert posts first, but will get regular posts when there are none
    else {
        options = { sort: { expertNeeded: -1 } }
    }
    TiktokUser.findOne(filter, null, options, function (err, user) {
        if (err) {
            console.log(err)
            return
        }
        if (!user) {
            console.log("no user found")
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify(null))
        }
        else {
            recentlySent.set(user.userId, 1)
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ userId: user.userId, numOfVideos: user.videos.length }))
        }
    })
})
router.get("/getVideos", (req, res) => {
    TiktokUser.findOne({ userId: req.query.userId }, function (err, user) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ videoIds: user.videos }))
    })
})

router.get("/video", (req, res) => {
    let videoID = req.query.id
    console.log(videoID)
    return res.render("tiktok.ejs", {
        id: videoID,
    });
})

router.post("/expert", (req, res) => {
    let userID = req.body.id;
    console.log(userID + "passed to expert");
    TiktokUser.findOne({ userId: userID }, function (err, user) {
        if (err) {
            console.log(err)
            return
        }
        user.expertNeeded = 1;
        user.save();
    })
    res.status(200).send();
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
    let userID = req.body.id
    let user_tag = req.body.user_tag
    let videos_tag = req.body.videos_tag
    let times_array = req.body.times_array
    let features = req.body.features;

    console.log(times_array + " times array");
    console.log(videos_tag + " videos tag");

    //update tiktokuser
    TiktokUser.findOne({ userId: userID }, async function (err, tiktokUser) {
        try {
            if (err) {
                console.log(err)
                return
            }
            let videosTags = [];
            let videos_pos_tags = 0;
            for (i = 0; i < videos_tag.length; i++) {
                videosTags.push({ timeDelta: times_array[i], features: features[i], decision: videos_tag[i] });
                videos_pos_tags += videos_tag[i] == true;
            }
            let tag = Tag({ videoTag: videosTags, userDecision: user_tag });
            tag.save();
            tiktokUser.tags.push(tag);
            tiktokUser.save();


            //update user
            let user = req.user;
            user.videos_tagged += videos_tag.length;
            user.weekly_tags_left -= videos_tag.length;
            user.user_pos_tags += user_tag == true;
            user.user_neg_tags += user_tag == false;
            user.user_total_tags += 1;
            user.videos_pos_tags += videos_pos_tags;
            user.videos_neg_tags += (videos_tag.length - videos_pos_tags);
            user.tags.push(tag.id)
            user.save();

            // update values
            await Value.findOneAndUpdate({ name: "user_pos_tags" }, { $inc: { value: user_tag == true } });
            await Value.findOneAndUpdate({ name: "user_neg_tags" }, { $inc: { value: user_tag == false } });
            await Value.findOneAndUpdate({ name: "user_total_tags" }, { $inc: { value: 1 } });
            await Value.findOneAndUpdate({ name: "videos_pos_tags" }, { $inc: { value: videos_pos_tags } });
            await Value.findOneAndUpdate({ name: "videos_neg_tags" }, { $inc: { value: videos_tag.length - videos_pos_tags } });
            await Value.findOneAndUpdate({ name: "videos_tagged" }, { $inc: { value: videos_tag.length } });
            await Value.findOneAndUpdate({ name: "videos_tagged_this_week" }, { $inc: { value: videos_tag.length } });
        } catch (err) {
            console.log(err);
        }
    })

    res.status(200).send();


})

router.get("/getValue", (req, res) => {
    Value.findOne({ name: req.query.name }, function (err, value) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ value: value }))
    })
})

module.exports = router;