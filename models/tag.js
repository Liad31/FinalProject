const { json } = require("express");

const Schema = mongoose.Schema;

const tagSchema = new Schema({
    video_id: { type: Schema.Types.ObjectId, ref: 'Video'},
    user_id: { type: Schema.Types.ObjectId, ref: 'User'},
    time_in_sec: {type:Number, required:true},
    features: {type:Object, required:true},
    createdAt: {type:Date, default:Date.now}
});


const Tag = mongoose.model("Tag", tagSchema);

module.exports = Tag;