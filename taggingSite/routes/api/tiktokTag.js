let express = require("express");
let router = express.Router();
const User = require("../../models/user")
const Tag = require("../../models/tag")
const TiktokUser = require("../../models/tiktokUserNationalistic");
const Stats = require("../../models/stats");
const Video = require("../../models/video");
const NodeCache = require("node-cache");
const { ObjectId } = require("bson");

router.get("/getVideos", (req, res) => {
    TiktokUser.findOne({ userId: req.query.userId }).populate('videos').exec(function (err, user) {
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