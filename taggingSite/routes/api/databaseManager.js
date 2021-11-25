var express = require("express");
var router = express.Router();
const User = require("../../models/user")
const Tag = require("../../models/tag")
const TiktokUser = require("../../models/tiktokUser");
const Stats = require("../../models/stats");
const Video = require("../../models/video");


router.post("/postNewUser", (req, res) => {
    let userID = req.body.id;
    let videos_arr = req.body.videos;
    let bio = req.body.bio;
    let governorate = req.body.governorate;
    let userStats =  req.body.userStats;
    let videos = []
    for (i = 0; i < videos_arr.length; i++) {
        let cur_video = Video({
            Vid: videos_arr[i]['Vid'],
            text: videos_arr[i]['text'],
            hashtags: videos_arr[i]['hashtags'],
            musicId: videos_arr[i]['musicId'],
            musicUrl: videos_arr[i]['musicUrl']
        });
        videos.push(cur_video);
        cur_video.save().catch(err => {
            res.status(400).send("unable to save to database");
          });
    }

    console.log(bio);
    let newUser = TiktokUser({
        userId: userID,
        videos: videos,
        bio : bio,
        governorate: governorate,
        userStats : userStats,
        tags: []
    });
    newUser.save()
    .then(item => {
        res.status(200).send("user saved");
      })
      .catch(err => {
        res.status(400).send("unable to save to database");
      });
    ;
    res.status(200).send();
})


module.exports = router;