var express = require("express");
var router = express.Router();
const TiktokUser = require("../../models/tiktokUserNationalistic");
const Video = require("../../models/video");



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
        for (let k = 0; k < req.body.users[t]['videos'].length && user.videos.length < 3; k++) {
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
        for (let i = 0; i < Math.min(videos_arr.length,3); i++) {
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
  for (let t = 0; t < req.body.users.length; t++) {
    let videoID = req.body.videos[t];
    Video.findOne({ Vid: videoID }, async function (err, video) {
      if (err) {
        console.log("Error:" + String(err));
        res.status(200).send("error occured");
      }
      if (video) {
        let video_text = req.body.texts[t];
        video.video_text = video_text;
        vid.save().catch(err => {
          res.status(400).send("unable to save to database");
        });
      }
    })
  }
  res.status(200).send();


})
router.get("/getVideos", (req, res) => {
  numVideos = Number(req.query.num)
  agg=[{
    '$match': {
      '$or': [
        {
          'downloaded': false
        }, {
          'videoText': 'ERROR!!!!!'
        }
      ]
    }
  }, {
    '$sample': {
      'size': numVideos
    }
  }
]
  Video.aggregate(agg ,function(err, videos){
    if (err) {
      console.log(`Error: ${err}`);
      res.status(200).send("error occured");
    }
    if (videos) {
      res.status(200).send(videos);
    }
  })
  // Video.find({downloaded: false}).limit(numVideos).exec(function (err, videos) {
  //   if (err) {
  //     console.log("Error:" + String(err));
  //     res.status(200).send("error occured");
  //   }
  //   if (videos) {
  //     res.status(200).send(videos);
  //   }
  // })
})
router.post("/markVideosDownloaded",  (req, res) => {
  for( video of req.body.videos){
    let videoID = video.Vid;
    let text= video.text;
    Video.updateMany({Vid: videoID}, {$set: {downloaded: true, videoText: text}}, function(err, video){
      if(err){
        console.log(`Error: ${err}`);
        res.status(200).send("error occured");
      }
    })
  }
  res.status(200).send();
})

module.exports = router;