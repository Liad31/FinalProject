let express = require("express");
let router = express.Router();
const User = require("../../models/user")
const Tag = require("../../models/tag")
const TiktokUser = require("../../models/tiktokUserNationalistic");
const Stats = require("../../models/stats");
const Video = require("../../models/video");
const NodeCache = require("node-cache");
const { ObjectId } = require("bson");

// TTL=30 mins
const recentlySent = new NodeCache({ stdTTL: 30*60*60, checkperiod: 0});

router.get("/getUser", (req, res) => {
    let perms = req.user.Permissions
    console.log(perms)
    // invalidate cache
    for( key of recentlySent.keys()){
        recentlySent.get(key)
    }
    let filter = {
        "tags.0": { $exists: false },
        userId: { $nin: recentlySent.keys() }
    }
    let options = {}
    filter.error = 0; // users marked in error won't bt given to tag
    // a regular user can't tag expert posts
    if (perms == 0) {
        filter.expertNeeded = {$eq: null}
        options = { sort: { userId: 1 } } //already inverted the order
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
            res.end(JSON.stringify({ userId: user.userId, numOfVideos: user.videos.length, message: user.expertNeeded, userName: user.userName}))
        }
    })
})

router.post("/expert", (req, res) => {
    let userID = req.body.id;
    let message = req.body.message;
    console.log(userID + "passed to expert");
    TiktokUser.findOne({ userId: userID }, function (err, user) {
        if (err) {
            console.log(err)
            return
        }
        user.expertNeeded = message;
        console.log(message)
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
    if (features === undefined) {
        features = [];
    }

    console.log(times_array + " times array");
    console.log(videos_tag + " videos tag");
    console.log(features + " features");

    //update tiktokuser
    TiktokUser.findOne({ userId: userID }, async function (err, tiktokUser) {
        try {
            if (err) {
                console.log(err)
                return
            }
            let videosTags = [];
            let videos_pos_tags = 0;
            let total_time = 0;
            for (let i = 0; i < videos_tag.length; i++) {
                videosTags.push({ timeDelta: times_array[i], features: features[i], decision: videos_tag[i] });
                videos_pos_tags += videos_tag[i] == true;
                total_time += parseFloat(times_array[i])
            }
            let tag = Tag({ videoTag: videosTags, userDecision: user_tag });
            tag.save();
            tiktokUser.tags.push(tag);
            tiktokUser.save();

            //update user
            let user = req.user;
            user.weekly_tags_left -= videos_tag.length;
            user.tags.push(tag.id)
            user.save();

            let date = new Date();
            date.setDate(date.getDate() - 7);
            //date.setMinutes(date.getMinutes() - 1);

            //update user weekly stats
            let userStats = await Stats.findOne({ userId: user.id }, null, {sort: {date: -1 }})
            if (userStats == null) {
                userStats = new Stats({ userId: user.id, date: new Date(), username: user.username });
            }
            let old_total_time = userStats.video_avg_tagging_time * userStats.videos_total_tags;
            userStats.user_pos_tags += user_tag == true;
            userStats.user_neg_tags += user_tag == false;
            userStats.user_total_tags += 1;
            userStats.videos_pos_tags += videos_pos_tags;
            userStats.videos_neg_tags += (videos_tag.length - videos_pos_tags);
            userStats.videos_total_tags += videos_tag.length;
            userStats.video_avg_tagging_time = (old_total_time + total_time) / userStats.videos_total_tags;
            userStats.save();

            // update weekly stats
            let stats = await Stats.findOne({ userId: null, date: { $gt: date } })
            if (stats == null) {
                stats = new Stats({ userId: null, date: new Date(), username: null });
            }
            old_total_time = stats.video_avg_tagging_time * stats.videos_total_tags;
            stats.user_pos_tags += user_tag == true;
            stats.user_neg_tags += user_tag == false;
            stats.user_total_tags += 1;
            stats.videos_pos_tags += videos_pos_tags;
            stats.videos_neg_tags += (videos_tag.length - videos_pos_tags);
            stats.videos_total_tags += videos_tag.length;
            stats.video_avg_tagging_time = (old_total_time + total_time) / stats.videos_total_tags;
            stats.save();

            //update user stats
            userStats = await Stats.findOne({ userId: user.id, date: null })
            if (userStats == null) {
                userStats = new Stats({ userId: user.id, date: null, username: user.username });
            }
            old_total_time = userStats.video_avg_tagging_time * userStats.videos_total_tags;
            userStats.user_pos_tags += user_tag == true;
            userStats.user_neg_tags += user_tag == false;
            userStats.user_total_tags += 1;
            userStats.videos_pos_tags += videos_pos_tags;
            userStats.videos_neg_tags += (videos_tag.length - videos_pos_tags);
            userStats.videos_total_tags += videos_tag.length;
            userStats.video_avg_tagging_time = (old_total_time + total_time) / userStats.videos_total_tags;
            userStats.save();

            // update stats
            stats = await Stats.findOne({ userId: null, date: null })
            if (stats == null) {
                stats = new Stats({ userId: null, date: null, username: null });
            }
            old_total_time = stats.video_avg_tagging_time * stats.videos_total_tags;
            stats.user_pos_tags += user_tag == true;
            stats.user_neg_tags += user_tag == false;
            stats.user_total_tags += 1;
            stats.videos_pos_tags += videos_pos_tags;
            stats.videos_neg_tags += (videos_tag.length - videos_pos_tags);
            stats.videos_total_tags += videos_tag.length;
            stats.video_avg_tagging_time = (old_total_time + total_time) / stats.videos_total_tags;
            stats.save();

        } catch (err) {
            console.log(err);
        }
    })

    res.status(200).send();


})

router.get("/userStats", (req, res) => {
    Stats.findOne({ userId: ObjectId(req.query.userId), date: null }, function (err, stats) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ stats }))
    })
})

router.get("/stats", (req, res) => {
    Stats.findOne({ userId: null, date: null }, function (err, stats) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ stats }))
    })
})

router.get("/weeklyUserStats", (req, res) => {
    Stats.find({ userId: ObjectId(req.query.userId), date: { $ne: null } }, {}, { sort: { 'date': -1 } }, function (err, stats) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ stats }));
    });
})

router.get("/weeklyStats", (req, res) => {
    Stats.find({ userId: null, date: { $ne: null } }, {}, { sort: { 'date': -1 } }, function (err, stats) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ stats }));
    });
})

router.get("/userIds",(req, res) => {
    User.find({}, {select: "_id"}, function (err, users) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({ users }));
    });
})
module.exports = router;