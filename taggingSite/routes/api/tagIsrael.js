let express = require("express");
let router = express.Router();
const User = require("../../models/user")
const Img = require("../../models/israelTag")
const { ObjectId } = require("bson");
const Stats = require("../../models/israelTaggingStat");


router.get("/getImage", (req, res) => {
    let filter = {
        "tagged": false,
    }
    let options = {}


    Img.findOne(filter, null, options, function (err, image) {
        if (err) {
            console.log(err)
            return
        }
        if (!image) {
            console.log("no image found")
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify(null))
        }
        else {
            res.setHeader('Content-Type', 'application/json');
            res.end(JSON.stringify({ imageID: image.id }))
        }
    })
})

router.post("/tag", async (req, res) => {
    let imageId = req.body.id
    let user_tag = req.body.tag

    let update = { tagged: true, decision: user_tag }
    try {
        Img.findOneAndUpdate({ id: imageId }, update, null, function (err, document) { console.log(document); });

        //updare user
        let user = req.user;
        user.weekly_tags_left -= 1;
        user.save();

        let date = new Date();
        date.setDate(date.getDate() - 7);

        //update user weekly stats
        let userStats = await Stats.findOne({ userId: user.id }, null, { sort: { date: -1 } })
        if (userStats == null) {
            userStats = new Stats({ userId: user.id, date: new Date(), username: user.username });
        }
        userStats.pos_tags += user_tag == true;
        userStats.neg_tags += user_tag == false;
        userStats.total_tags += 1;
        userStats.save();

        // update weekly stats
        let stats = await Stats.findOne({ userId: null, date: { $gt: date } })
        if (stats == null) {
            stats = new Stats({ userId: null, date: new Date(), username: null });
        }
        stats.pos_tags += user_tag == true;
        stats.neg_tags += user_tag == false;
        stats.total_tags += 1;
        stats.save();

        //update user stats
        userStats = await Stats.findOne({ userId: user.id, date: null })
        if (userStats == null) {
            userStats = new Stats({ userId: user.id, date: null, username: user.username });
        }
        userStats.pos_tags += user_tag == true;
        userStats.neg_tags += user_tag == false;
        userStats.total_tags += 1;
        userStats.save();

        // update stats
        stats = await Stats.findOne({ userId: null, date: null })
        if (stats == null) {
            stats = new Stats({ userId: null, date: null, username: null });
        }
        stats.pos_tags += user_tag == true;
        stats.neg_tags += user_tag == false;
        stats.total_tags += 1;
        stats.save();
    } catch {
        res.status(404).send();
    }

    res.status(200).send();


})

module.exports = router;
