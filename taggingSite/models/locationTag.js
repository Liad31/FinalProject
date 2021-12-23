const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const locationTagSchema = new Schema({
    decision: Boolean,
});


const LocationTag = mongoose.model("locationTag", locationTagSchema);

module.exports = LocationTag;