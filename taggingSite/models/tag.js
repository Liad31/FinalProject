const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const tagSchema = new Schema({
    videoTag: [{ timeDelta: Number, features: Object, decision: Boolean}],
    userDecision: Boolean,
});


const Tag = mongoose.model("Tag", tagSchema);

module.exports = Tag;