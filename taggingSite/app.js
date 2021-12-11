//const fs = require('fs');
//const http = require('http');
//const https = require('https');
// var key = fs.readFileSync('./key.pem');
// var cert = fs.readFileSync('./cert.pem');
// var options = {
//   key: key,
//   cert: cert
// };
const schedule = require('node-schedule');
const mongoose = require("mongoose");
const express = require('express');
const path = require("path");
const cookieParser = require("cookie-parser");
const passport = require("passport");
const session = require("express-session");
const flash = require("connect-flash");
const params = require("./params/params");
const bodyParser = require("body-parser");
const setUpPassport = require("./setuppassport");
const User = require('./models/user');
const Stats = require('./models/stats');

const app = express();
mongoose.connect(params.DATABASECONNECTION);
setUpPassport();
//const httpServer = http.createServer(app);
//httpServer.listen(8000);

app.set("port", process.env.PORT || 8001);
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(cookieParser());
app.use(session({
    secret: "dogdfgdnk5n34knfeopg",
    resave: false,
    saveUninitialized: false
}));
app.use(passport.initialize());
app.use(passport.session());
app.use(flash());
app.use(express.static(__dirname+'/public'));
app.use(express.urlencoded({extended: true}))
// app.use(express.static('./views'))
app.use(express.json({extended: true}));
// app.use(express.urlencoded({ extended: true }));
app.use("/", require("./routes/web")); // using the router from web/index.js
app.use("/api", require("./routes/api"));

// const job = schedule.scheduleJob(params.WEKKLY_UPDATE_TIME, async function(){
//     let res = await User.updateMany({}, {"$inc": {weekly_tags_left: params.WEEKLY_TAGS_NUM}});

//     let today = new Date();
//     let users = await User.find({});
//     for (let user of users) {
//        (new Stats({date: today, userId: user.id})).save();
//     }
//     (new Stats({date: today, userId: null})).save();
// });
//TODO: change this bacl

app.listen(app.get("port"), () => {
    console.log(`Starting on port ${app.get("port")}`);
})