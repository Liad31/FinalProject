const fs = require('fs');
const http = require('http');
//const https = require('https');
// var key = fs.readFileSync('./key.pem');
// var cert = fs.readFileSync('./cert.pem');
// var options = {
//   key: key,
//   cert: cert
// };
const express = require('express');
const app = express();

const httpServer = http.createServer(app);

httpServer.listen(8000);

app.use(express.urlencoded({
    extended: false
}))

app.use(express.static('./templates'))
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
    
app.get("/", (req, res)=>{
    res.sendFile("templates/logIn.html", { root: '.' })
})

app.get("/signUp", (req, res)=>{
    res.sendFile("templates/signUp.html", { root: '.' })
})

app.post("/sign", (req, res)=>{
    let email = console.log(req.body.email)
    let psw = console.log(req.body.psw)
    let psw_repeat = console.log(req.body.psw_repeat)

})

app.get("/home", (req, res)=>{
    //send the url, video-id as parameters
    res.sendFile('templates/home.html',{root:'.'});
})











app.listen(8001)