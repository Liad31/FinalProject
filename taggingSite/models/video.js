const { ObjectId } = require("mongodb");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const videoSchema = new Schema({
    Vid: String,
    text: String, 
    hashtags: [{type: String}], 
    musicId: String, 
    musicUrl: String,
    date: String,
    downloaded: {type: Boolean, default: false},
    videoText: {type: String, default: ""},
    stats: Object,
    user: {type: ObjectId, default: null},
    score: {type: Number, default: -1}
});

const Video = mongoose.model("Video", videoSchema);

module.exports = Video;