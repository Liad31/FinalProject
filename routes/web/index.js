const router = require("express").Router();




router.use(function(req, res, next) {
    res.locals.currentUser = req.user;
    console.log("!!!!!!!!!!");
    console.log(req.user);
    next();
});

router.use("/", require("./home"));


module.exports = router;
