var express = require("express");
var router = express.Router();
const User= require("../../models/user")
const Tag= require("../../models/tag")
const TiktokUser= require("../../models/tiktokUser");
const NodeCache= require("node-cache");
// TTL=30 mins
const recentlySent= new NodeCache({stdTTL: 1});// change back to 30 min!!!!!!!!!!!!!!!!!!!
router.get("/", (req,res)=> {
    let user=TiktokUser({
        userId: "@arabushKashe",
        videos: ["1","2"],
        tags: [],
        expertNeeded: true
    })  
    user.save()
})
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

module.exports = router;