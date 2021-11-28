var express = require("express");
var router = express.Router();
const User = require("../../models/user")
const Tag = require("../../models/tag")
const TiktokUser = require("../../models/tiktokUser");
const Stats = require("../../models/stats");
const Video = require("../../models/video");



router.post("/postNewUsers", (req, res) => {
  for (let t = 0; t < req.body.users.length;t++){
    let userID = req.body.users[t]['id'];
    TiktokUser.findOne({ userId: userID }, function (err, user) {
      if (err) {
        console.log(`Error: ${err}`);
        res.status(200).send("error occured");
      }
      if (user) {
        console.log("adding videos to user");
        for (let k = 0; k < req.body.users[t]['videos'].length; k++) {
          videoID = req.body.users[t]['videos'][k]['Vid']
          Video.findOne({ Vid: videoID }, function (err, video) {
            if (err) {
              console.log(`Error: ${err}`);
              res.status(200).send("error occured");
            }
            if (video) {
            }
            else {
              videos=req.body.users[t]['videos']
              let vid = Video({
                Vid: videos[k]['Vid'],
                text: videos[k]['text'],
                hashtags: videos[k]['hashtags'],
                musicId: videos[k]['musicId'],
                musicUrl: videos[k]['musicUrl']
              });
              user.videos.push(vid).then(function (value) {
                user.save().catch(err => {
                  res.status(400).send("unable to save to database");
                });
              });
              vid.save().catch(err => {
                res.status(400).send("unable to save to database");
              });
            }
          });
        }
      }
      else {
        console.log(t);
        let videos_arr = req.body.users[t]['videos'];
        let bio = req.body.users[t]['bio'];
        let governorate = req.body.users[t]['governorate'];
        let userStats =  req.body.users[t]['userStats'];
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
        console.log("adding new user");
        let newUser = TiktokUser({
          userId: userID,
          videos: videos,
          bio : bio,
          governorate: governorate,
          userStats : userStats,
          tags: []
        });
        newUser.save().catch(err => {
          res.status(400).send("unable to save to database");
        });
      }
    })
  }
  res.status(200).send();
})


module.exports = router;