var express = require("express");
var router = express.Router();
const TiktokUser = require("../../models/tiktokUserNationalistic");
const Video = require("../../models/video");
const Img= require("../../models/israelTag");


router.post("/postNewUsers", (req, res) => {
  for (let t = 0; t < req.body.users.length; t++) {
    let userID = req.body.users[t]['id'];
    TiktokUser.findOne({ userId: userID }, function (err, user) {
      if (err) {
        console.log(`Error: ${err}`);
        res.status(200).send("error occured");
      }
      if (user) {
        console.log("adding videos to user");
        let ids = req.body.users[t]['videos'].map(function (item) {
            return item.Vid;
        });
        Video.find({ Vid: { $in: ids } }, function (err, databaseVids) {
            if (err) {
                console.log(`Error: ${err}`);
            }
            for(let video of req.body.users[t]['videos']){
                if(databaseVids.map(vid=> vid.Vid).indexOf(video.Vid)!=-1)
                    continue
                let videoDoc=new Video({
                  Vid: video.Vid,
                  text: video.text,
                  date: video.date,
                  hashtags: video.hashtags,
                  musicId: video.musicId,
                  musicUrl: video.musicUrl,
                  stats: video.stats,
                  user: user._id,
                });
                user.videos.push(videoDoc);
                videoDoc.save().catch(err => {
                    console.log(`Error: ${err}`);
                })
            }
            user.save().catch(err => {
                console.log(`Error: ${err}`);
            })
          
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
        console.log("adding new user");
        let newUser = TiktokUser({
          userId: userID,
          videos: null,
          bio: bio,
          userName: user_name,
          governorate: governorate,
          userStats: userStats,
          tags: []
        });
        for (let i = 0; i < videos_arr.length; i++) {
          let cur_video = Video({
            Vid: videos_arr[i]['Vid'],
            text: videos_arr[i]['text'],
            date: videos_arr[i]['date'],
            hashtags: videos_arr[i]['hashtags'],
            musicId: videos_arr[i]['musicId'],
            musicUrl: videos_arr[i]['musicUrl'],
            stats: videos_arr[i]['stats'],
            user: newUser._id
          });
          videos.push(cur_video);
          cur_video.save().catch(err => {
            res.status(400).send("unable to save to database");
          });
        }
        newUser.videos = videos;
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
      '$and': [
        {
          // videoText:"ERROR!!!!!"
          downloaded: false,
          // inBatch: true
        }
        // {
        // 'videoText': "Unproced"
        // }
        // {
        //   'videoText': 'ERROR2!!!!!'
        // }
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
})

router.get("/getDownloadedVideos", (req, res) => {
  numVideos = Number(req.query.num)
  agg=[{
    '$match': {
      '$and': [
        {
        'videoText': "Unproced"
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
router.post("/postNewImage", (req, res) => {
  let id=req.body.id;
  img=Img({id:id})
  img.save().catch(err => {
    console.log(`Error: ${err}`);
  })
  res.status(200).send();
})

module.exports = router;