const { ObjectId } = require("bson");
const { json } = require("express");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const nationalisticTaggingStatSchema = new Schema({
    userId: {type:ObjectId},
    username: {type:String, default: ""},
    date: {type:Date},
    user_pos_tags: {type:Number, default:0},
    user_neg_tags: {type:Number, default:0},
    user_total_tags: {type:Number, default:0},
    videos_pos_tags: {type:Number, default:0},
    videos_neg_tags: {type:Number, default:0},
    videos_total_tags: {type: Number, default:0},
    video_avg_tagging_time: {type:Number, default:0}
});


const NationalisticTaggingStat = mongoose.model("nationalisticTaggingStat", nationalisticTaggingStatSchema);
module.exports= NationalisticTaggingStat;