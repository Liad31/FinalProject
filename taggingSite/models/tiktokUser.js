const { json } = require("express");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tiktokUserSchema= new Schema({
    userId: String,
    videos: [{type: String}],
    tags: [{ type: Schema.Types.ObjectId, ref: 'Tag'}],
    expertNeeded: {type: Boolean, default: false},
    error: {type: Number, default: 0},
});


const TiktokUsers= mongoose.model("tiktokUsers", tiktokUserSchema);
module.exports=TiktokUsers
