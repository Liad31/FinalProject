const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tiktokUserLocationSchema= new Schema({
    userId: String,
    videos: [{ type: Schema.Types.ObjectId, ref: 'Video'}],
    bio: String,
    governorate: String,
    userStats: Object,
    userName: String,
    tags: [{ type: Schema.Types.ObjectId, ref: 'Tag'}],
    expertNeeded: {type: String, default: null},
    error: {type: Number, default: 0},
});


const TiktokUserLocation = mongoose.model("tiktokUserLocation", tiktokUserLocationSchema);
module.exports=TiktokUserLocation
