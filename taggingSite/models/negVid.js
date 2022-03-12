const { ObjectId } = require("mongodb");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const negVidSchema= new Schema({
    vid: ObjectId,
    expertTag: {type: Number, default: null}
});


const NegVid = mongoose.model("negVid", negVidSchema);
module.exports=NegVid
