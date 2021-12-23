const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const israelTagSchema = new Schema({
    id: String,
    tagged:  {type: Boolean, default: false},
    decision: Boolean,
});


const IsraelTag = mongoose.model("israelTag", israelTagSchema);

module.exports = IsraelTag;