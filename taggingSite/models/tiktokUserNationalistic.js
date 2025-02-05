const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tiktokUserNationalisticSchema= new Schema({
    userId: String,
    videos: [{ type: Schema.Types.ObjectId, ref: 'Video'}],
    bio: String,
    governorate: String,
    userStats: Object,
    userName: String,
    tags: [{ type: Schema.Types.ObjectId, ref: 'Tag'}],
    expertNeeded: {type: String, default: null},
    error: {type: Number, default: 0},
    num_videos_tagged: {type: Number, default: 0},
    userStats: Object
});


const TiktokUserNationalistic = mongoose.model("tiktokUserNationalistic", tiktokUserNationalisticSchema);
module.exports=TiktokUserNationalistic
