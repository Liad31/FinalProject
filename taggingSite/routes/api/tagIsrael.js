let express = require("express");
let router = express.Router();
const User = require("../../models/user")
const Img = require("../../models/israelTag")
const { ObjectId } = require("bson");

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
            res.end(JSON.stringify({ imageID: image.id}))
        }
    })
})

router.post("/tag", async (req, res) => {
    let imageId = req.body.id
    let user_tag = req.body.tag

    let update = {tagged: true, decision: user_tag}
    try {
        Img.findOneAndUpdate({ id: imageId }, update, null, function (err, document) {console.log(document);});


        let user = req.user;
        user.weekly_tags_left -= 1;
        user.save();
    } catch {
        res.status(404).send();

    }

    res.status(200).send();


})

module.exports = router;
