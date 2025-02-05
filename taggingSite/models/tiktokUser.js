const { json } = require("express");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tiktokUserSchema= new Schema({
    userId: String,
    userName: String,
    videos: [{ type: Schema.Types.ObjectId, ref: 'Video'}],
    bio: String,
    governorate: String,
    userStats: Object,
    tags: [{ type: Schema.Types.ObjectId, ref: 'Tag'}],
    expertNeeded: {type: String, default: null},
    error: {type: Number, default: 0},
});


const TiktokUsers= mongoose.model("tiktokUsers", tiktokUserSchema);
module.exports=TiktokUsers
