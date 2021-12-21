var express = require("express");

var router = express.Router();

router.use(function(req, res, next) {
    res.locals.currentUser = req.user;
    res.locals.error = req.flash("error");
    res.locals.info = req.flash("info");
    next();
});

router.use("/tagLocation", require("./tagLocation"));
router.use("/tagNationalistic", require("./tagNationalistic"));
router.use("/tagIsrael", require("./tagIsrael"));
router.use("/tiktokTag", require("./tiktokTag"));
router.use("/database", require("./databaseManager"));


module.exports = router;    