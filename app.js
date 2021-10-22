//const fs = require('fs');
//const http = require('http');
//const https = require('https');
// var key = fs.readFileSync('./key.pem');
// var cert = fs.readFileSync('./cert.pem');
// var options = {
//   key: key,
//   cert: cert
// };
const express = require('express');
const path = require("path");

const app = express();
//const httpServer = http.createServer(app);
//httpServer.listen(8000);

app.set("port", process.env.PORT || 8000);
app.set("views", path.join(__dirname, "views"));
app.set("view engine", "ejs");

app.use(express.static('public'));
// app.use(express.urlencoded({
//     extended: false
// }))
// app.use(express.static('./views'))
// app.use(express.json());
// app.use(express.urlencoded({ extended: true }));
app.use("/", require("./routes/web")); // using the router from web/index.js
//app.use("/api", require("./routes/api"));


app.listen(app.get("port"), () => {
    console.log(`Starting on port ${app.get("port")}`);
})