const { json } = require("express");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tiktokUserSchema= new Schema({
    userId: String,
    videos: [{type: String}],
    tags: [{ type: Schema.Types.ObjectId, ref: 'Tag'}],
    expertNeeded: {type: Boolean, default: false},
});


const TiktokUsers= mongoose.model("tiktokUsers", tiktokUserSchema);
module.exports=TiktokUsers
