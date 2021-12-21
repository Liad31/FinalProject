let express = require("express");
let router = express.Router();
const TiktokUser = require("../../models/tiktokUserNationalistic");

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