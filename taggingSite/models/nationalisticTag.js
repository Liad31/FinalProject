const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const nationalisticTagSchema = new Schema({
    videoTag: [{ timeDelta: Number, features: Object, decision: Number}],
    userDecision: Boolean,
});


const NationalisticTag = mongoose.model("nationalisticTag", nationalisticTagSchema);

module.exports = NationalisticTag;