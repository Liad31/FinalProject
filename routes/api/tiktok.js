var express = require("express");
var router = express.Router();
const User= require("../../models/user")
const Tag= require("../../models/tag")
const TiktokUser= require("../../models/tiktokUser");
const NodeCache= require("node-cache");
// TTL=30 mins
const recentlySent= new NodeCache({stdTTL: 1});// change back to 30*60*60 min!!!!!!!!!!!!!!!!!!!

router.post("/submitTag", (req,res) => {
    let params=req.body
})
router.get("/getUser", (req,res) => {
    let perms= req.user.Permissions
    console.log(perms)
    let filter={
        "tags.0":{$exists: false},
        userId: {$nin: recentlySent.keys()}  
    }
    let options={}
    // a regular user can't tag expert posts
    if(perms==0){
        filter.expertNeeded = 0
    }
    //an expert needs to see expert posts first, but will get regular posts when there are none
    else{
        options={sort: {expertNeeded: -1}}
    }
    TiktokUser.findOne(filter, null, options, function(err,user){
        if(err){
            console.log(err)
            return
        }
        if (!user) {
            console.log("no user found")
            return
        }
        recentlySent.set(user.userId,1)
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({userId: user.userId, numOfVideos: user.videos.length}))
    })
})
router.get("/getVideos", (req,res) => {
    TiktokUser.findOne({userId: req.query.userId}, function(err,user){
        if(err){
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({videoIds: user.videos}))
    })
})

router.get("/video", (req,res) => {
    let videoID = req.query.id
    console.log(videoID)
    return res.render("tiktok.ejs", {
        id: videoID,
      });

})

router.post("/expert", (req,res) => {
    let userID = req.body.id
    console.log(userID + "passed to expert")
    TiktokUser.findOne({userId: userID}, function(err,user){
        if(err){
            console.log(err)
            return
        }
        // save that the user was passed to expert
    })
    res.status(200).send();


})

router.post("/tag", (req,res) => {
    let userID = req.body.id
    let user_tag = req.body.user_tag
    let videos_tag = req.body.videos_tag
    console.log(userID + "passed to expert")
    TiktokUser.findOne({userId: userID}, function(err,user){
        if(err){
            console.log(err)
            return
        }
        // save the tags
    })
    res.status(200).send();


})

module.exports = router;