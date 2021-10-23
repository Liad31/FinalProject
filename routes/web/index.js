const router = require("express").Router();




router.use(function(req, res, next) {
    res.locals.currentUser = req.user;
    res.locals.error = req.flash("error");
    res.locals.info = req.flash("info");
    next();
});

router.use("/", require("./home"));
router.use("/tag", require("./tag"));

module.exports = router;
