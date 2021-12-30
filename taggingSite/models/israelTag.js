const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const israelTagSchema = new Schema({
    id: String,
    tagged:  {type: Boolean, default: false},
    decision: Boolean,
    downloaded: {type: Boolean, default: false},
});


const IsraelTag = mongoose.model("israelTag", israelTagSchema);

module.exports = IsraelTag;