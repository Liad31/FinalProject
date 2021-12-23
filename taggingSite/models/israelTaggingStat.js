const { ObjectId } = require("bson");
const { json } = require("express");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const israelTaggingStatSchema = new Schema({
    userId: {type:ObjectId},
    username: {type:String, default: ""},
    date: {type:Date},
    pos_tags: {type:Number, default:0},
    neg_tags: {type:Number, default:0},
    total_tags: {type:Number, default:0},
});


const IsraelTaggingStat = mongoose.model("israelTaggingStat", israelTaggingStatSchema);
module.exports= IsraelTaggingStat;