const { json } = require("express");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const videoSchema = new Schema({
    tags: [{ type:Schema.Types.ObjectId, ref: 'Tag'}],
    tiktok_id: { type:String, required:true},
});


const ExpertVideos= mongoose.model("ExpertVideos", videoSchema);
const Video = mongoose.model("Video", videoSchema);
module.exports={
    Video: Video,
    ExpertVideos: ExpertVideos 
}