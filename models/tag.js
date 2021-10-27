const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tagSchema = new Schema({
    videoTag: [{tiktokId: String, timeDelta: Number, features: Object, decision: Number}],
    videoDecision: Number,
});


const Tag = mongoose.model("Tag", tagSchema);

module.exports = Tag;