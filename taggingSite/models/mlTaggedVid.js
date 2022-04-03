const { ObjectId } = require("mongodb");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const mlTaggedVidSchema= new Schema({
    vid: ObjectId,
    expertTag: {type: Number, default: null},
    prediction: {type: Number, default: null}
});


const mlTaggedVid = mongoose.model("negVid", mlTaggedVidSchema);
module.exports=mlTaggedVid
