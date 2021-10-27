var express = require("express");

var router = express.Router();

router.use("/tiktok", require("./tiktok.js"));

module.exports = router;