const router = require("express").Router();
const ensureAuthenticated = require("../../auth/auth").ensureAuthenticated;

router.use(ensureAuthenticated);

router.get("/", function(req, res) {
    res.render("tag")
})






module.exports = router;