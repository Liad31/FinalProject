const router=require("home").router
const User= require("../../models/user")
const Tag= require("../../models/tag")
const tiktokUsers= require("../../models/tiktokUser");
const NodeCache= require("node-cache");
// TTL=30 mins
const recentlySent= new NodeCache({stdTTL: 30*60*60});

// input format:
// 
router.post("api/submitTag", (req,res) => {
    let params=req.body
})
router.get("api/getUser", (req,res) => {
    let isExpert=req.query.expert
    // const tagsPerUser=1
    // const tagToFind= "tags."+(tagsPerUser-1)
    const filter={
        expertNeeded: isExpert,
        "tags.0":{$exists: false},
        userId: {$nin: recentlySent.keys()}  
    }
    tiktokUsers.findOne(filter, function(err,user){
        if(err){
            console.log(err)
            return
        }
        recentlySent.set(user.userId,1)
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({userId: user.userId, numOfVideos: user.Videos.length}))
    })
})
router.get("api/getVideos", (req,res) => {
    tiktokUsers.findOne({userId: req.query.userId}, function(err,user){
        if(err){
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify({videoIds: user.videos}))
    })
})