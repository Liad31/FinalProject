var express = require("express");
var router = express.Router();
const TiktokUser = require("../../models/tiktokUserLocation");
const Video = require("../../models/video");
const Img = require("../../models/israelTag")

router.post("/postNewImage", (req, res) => {
    let id = req.body.id;
    let img= Img({id:id});
    img.save().catch(console.error);
    console.log(id)
    res.status(200).send();
})
router.post("/postNewUsers", (req, res) => {
  for (let t = 0; t < req.body.users.length; t++) {
    let userID = req.body.users[t]['id'];
    TiktokUser.findOne({ userId: userID }, function (err, user) {
      if (err) {
        console.log(`Error: ${err}`);
        res.status(200).send("error occured");
      }
      if (user) {
        video_saved = 0
        console.log("adding videos to user");
        for (let k = 0; k < req.body.users[t]['videos'].length && user.videos.length < 6; k++) {
          videoID = req.body.users[t]['videos'][k]['Vid']
          Video.findOne({ Vid: videoID }, async function (err, video) {
            if (err) {
              console.log(`Error: ${err}`);
              res.status(200).send("error occured");
            }
            if (video) {
            }
            else {
              videos = req.body.users[t]['videos']
              let vid = Video({
                Vid: videos[k]['Vid'],
                text: videos[k]['text'],
                hashtags: videos[k]['hashtags'],
                musicId: videos[k]['musicId'],
                musicUrl: videos[k]['musicUrl'],
                date: videos[k]['date']
              });
              console.log(vid)
              console.log(user.videos)
              user.videos.push(vid);
              await vid.save().catch(err => {
                res.status(400).send("unable to save to database");
              });
            }
          })
        }
        user.save().catch(err => {
          res.status(400).send("unable to save to database");
        });
      }
      else {
        console.log(t);
        let videos_arr = req.body.users[t]['videos'];
        let bio = req.body.users[t]['bio'];
        let user_name = req.body.users[t]['userName'];
        let governorate = req.body.users[t]['governorate'];
        let userStats = req.body.users[t]['userStats'];
        let videos = []
        for (let i = 0; i < videos_arr.length && user.videos.length < 6; i++) {
          let cur_video = Video({
            Vid: videos_arr[i]['Vid'],
            text: videos_arr[i]['text'],
            date: videos_arr[i]['date'],
            hashtags: videos_arr[i]['hashtags'],
            musicId: videos_arr[i]['musicId'],
            musicUrl: videos_arr[i]['musicUrl'],
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
          bio: bio,
          userName: user_name,
          governorate: governorate,
          userStats: userStats,
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

//gets a list of video ids
router.post("/addVideoText", (req, res) => {
  for (video of req.body.videos) {
    videoID=video['Vid']
    videoText= video['text']
    Video.findOne({ Vid: videoID }, async function (err, video) {
      if (err) {
        console.log("Error:" + String(err));
        res.status(200).send("error occured");
      }
      if (video) {
        video.video_text = videoText;
        video.downloaded = true;
        video.save().catch(err => {
          res.status(400).send("unable to save to database");
        });
      }
    })
  }
  res.status(200).send();
})
router.get("/getVideos", (req, res) => {
numVideos = Number(req.query.num)
  Video.find().limit(numVideos).exec(function (err, videos) {
    if (err) {
      console.log("Error:" + String(err));
      res.status(200).send("error occured");
    }
    if (videos) {
      res.status(200).send(videos);
    }
  })
})

router.post("/markVideosDownloaded",  (req, res) => {
  for (let t = 0; t < req.body.videos.length; t++) {
    let videoID = req.body.videos[t];
    Video.findOneAndUpdate({ Vid: videoID }, { downloaded: true })
  } 
})

module.exports = router;