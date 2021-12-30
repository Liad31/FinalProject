const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const featureCounterSchema = new Schema({
    feature: {type: String, required:true, unique: true},
    counter:  {type: Number, default: 0},
});


const FeatureCounter = mongoose.model("featureCounter", featureCounterSchema);

module.exports = FeatureCounter;