const { json } = require("express");

const Schema = mongoose.Schema;

const videoSchema = new Schema({
    tags: [{ type:Schema.Types.ObjectId, ref: 'Tag'}],
    tiktok_id: { type:Number, required:true},
});


const Video = mongoose.model("Video", videoSchema);

module.exports = Video;