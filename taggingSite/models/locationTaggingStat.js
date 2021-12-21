const { ObjectId } = require("bson");
const { json } = require("express");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const locationTaggingStatSchema = new Schema({
    userId: {type:ObjectId},
    username: {type:String, default: ""},
    date: {type:Date},
    user_pos_tags: {type:Number, default:0},
    user_neg_tags: {type:Number, default:0},
    user_total_tags: {type:Number, default:0},
});


const LocationTaggingStat = mongoose.model("locationTaggingStat", locationTaggingStatSchema);
module.exports= LocationTaggingStat;