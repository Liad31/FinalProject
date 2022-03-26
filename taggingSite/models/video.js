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
    stats: Object
});

const Video = mongoose.model("Video", videoSchema);

module.exports = Video;