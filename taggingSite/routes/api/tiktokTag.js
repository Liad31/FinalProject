let express = require("express");
let router = express.Router();
const TiktokUser = require("../../models/tiktokUserNationalistic");
const TiktokUserLoc= require("../../models/tiktokUserLocation");
const MAX_VIDEOS_PER_TAG = require("../../params/params").MAX_VIDEOS_PER_TAG;
router.get("/getVideos", (req, res) => {
    TiktokUser.findOne({ userId: req.query.userId }).populate('videos').exec(function (err, user) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        ids = []
        // console.log("num videos tageed: ",user.num_videos_tagged)
        // console.log("num videos: ", user.videos.length)
        for (let i = user.num_videos_tagged; i < Math.min(user.videos.length, user.num_videos_tagged + MAX_VIDEOS_PER_TAG); i++) {
            ids.push(user.videos[i].Vid)
        }
        // console.log(ids)
        res.end(JSON.stringify({ videoIds: ids }))
    })
})

router.get("/getVideosLoc", (req, res) => {
    TiktokUserLoc.findOne({ userId: req.query.userId }).populate('videos').exec(function (err, user) {
        if (err) {
            console.log(err)
            return
        }
        res.setHeader('Content-Type', 'application/json');
        ids = []
        for (let i = 0; i < user.videos.length; i++) {
            ids.push(user.videos[i].Vid)
        }
        res.end(JSON.stringify({ videoIds: ids }))
    })
})
router.get("/video", (req, res) => {
    let videoID = req.query.id
    console.log(videoID, "videoID")
    return res.render("tiktok.ejs", {
        id: videoID,
    });
})

module.exports = router;