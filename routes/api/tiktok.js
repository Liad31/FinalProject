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
        userId: "123",
        videos: ["1","17","pastrama"],
        tags: []
    })
    user.save()
})
// input format:
// 
router.post("/submitTag", (req,res) => {
    let params=req.body
})
router.get("/getUser", (req,res) => {
    let Permissions = req.user.Permissions
    console.log(Permissions)
    // const tagsPerUser=1
    // const tagToFind= "tags."+(tagsPerUser-1)
    const filter={
        expertNeeded: Permissions > 0,
        "tags.0":{$exists: false},
        userId: {$nin: recentlySent.keys()}  
    }
    TiktokUser.findOne(filter, function(err,user){
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