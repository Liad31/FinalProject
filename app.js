//const fs = require('fs');
//const http = require('http');
//const https = require('https');
// var key = fs.readFileSync('./key.pem');
// var cert = fs.readFileSync('./cert.pem');
// var options = {
//   key: key,
//   cert: cert
// };
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
app.use(express.static('public'));
app.use(express.urlencoded({extended: true}))
// app.use(express.static('./views'))
app.use(express.json({extended: true}));
// app.use(express.urlencoded({ extended: true }));
app.use("/", require("./routes/web")); // using the router from web/index.js
//app.use("/api", require("./routes/api"));



app.listen(app.get("port"), () => {
    console.log(`Starting on port ${app.get("port")}`);
})