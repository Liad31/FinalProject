const fs = require('fs');
//const http = require('http');
//const https = require('https');
// var key = fs.readFileSync('./key.pem');
// var cert = fs.readFileSync('./cert.pem');
// var options = {
//   key: key,
//   cert: cert
// };
const express = require('express');
const app = express();
const path = require("path");

//const httpServer = http.createServer(app);
//httpServer.listen(8000);

app.set("port", process.env.PORT || 8000);
app.listen(app.get("port"), () => {
    console.log(`Starting on port ${app.get("port")}`);
})
app.use(express.static('public'));
app.use(express.urlencoded({
    extended: false
}))

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");
app.use(express.static('./views'))
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
    
app.get("/", (req, res)=>{
    res.render("logIn.ejs");
})

app.get("/signUp", (req, res)=>{
    res.render("signUp.ejs");
})

app.post("/sign", (req, res)=>{
    let email = console.log(req.body.email)
    let psw = console.log(req.body.psw)
    let psw_repeat = console.log(req.body.psw_repeat)

})

app.get("/home", (req, res)=>{
    //send the url, video-id as parameters
    res.render("home.ejs");
})











app.listen(8001)