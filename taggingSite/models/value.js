const { json } = require("express");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const ValueSchema= new Schema({
    name: {type:String, unique:true},
    value: {type:Number, default:0},
});


const Value = mongoose.model("Value", ValueSchema);
module.exports= Value;