const router = require("express").Router();
const ensureAuthenticated = require("../../auth/auth").ensureAuthenticated;

router.use(ensureAuthenticated);

router.get("/", (req, res) => {
    //send the url, video-id as parameters
    res.render("home.ejs");
    console.log("getting home page");
});





module.exports = router;