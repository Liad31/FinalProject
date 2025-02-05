let express = require("express");
let router = express.Router();
const User = require("../../models/user")
const Tag = require("../../models/locationTag")
const TiktokUser = require("../../models/tiktokUserLocation");
const Stats = require("../../models/locationTaggingStat");
const Video = require("../../models/video");
const NodeCache = require("node-cache");
const { ObjectId } = require("bson");


// TTL=30 mins
const recentlySent = new NodeCache({ stdTTL: 30*60*60, checkperiod: 0});

router.get("/getUser", (req, res) => {
    let perms = req.user.Permissions
    // console.log(perms)
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
        options = { sort: { _id: 1 } } 
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
    // console.log(userID + "passed to expert");
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

    //update tiktokuser
    TiktokUser.findOne({ userId: userID }, async function (err, tiktokUser) {
        try {
            if (err) {
                console.log(err)
                return
            }
            let tag = Tag({ decision: user_tag });
            tag.save();
            tiktokUser.tags.push(tag);
            tiktokUser.save();
            
            //update user
            let user = req.user;
            user.weekly_tags_left -= 1;
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
            userStats.user_pos_tags += user_tag == true;
            userStats.user_neg_tags += user_tag == false;
            userStats.user_total_tags += 1;
            userStats.save();

            // update weekly stats
            let stats = await Stats.findOne({ userId: null, date: { $gt: date } })
            if (stats == null) {
                stats = new Stats({ userId: null, date: new Date(), username: null });
            }
            stats.user_pos_tags += user_tag == true;
            stats.user_neg_tags += user_tag == false;
            stats.user_total_tags += 1;
            stats.save();

            //update user stats
            userStats = await Stats.findOne({ userId: user.id, date: null })
            if (userStats == null) {
                userStats = new Stats({ userId: user.id, date: null, username: user.username });
            }
            userStats.user_pos_tags += user_tag == true;
            userStats.user_neg_tags += user_tag == false;
            userStats.user_total_tags += 1;
            userStats.save();

            // update stats
            stats = await Stats.findOne({ userId: null, date: null })
            if (stats == null) {
                stats = new Stats({ userId: null, date: null, username: null });
            }
            stats.user_pos_tags += user_tag == true;
            stats.user_neg_tags += user_tag == false;
            stats.user_total_tags += 1;
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