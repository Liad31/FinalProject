const router = require("express").Router();
const ensureAuthenticated = require("../../auth/auth").ensureAuthenticated;
const params = require("../../params/params");


router.use(ensureAuthenticated);

// router.get("/", function(req, res) {
//     res.render("tag")
// })

router.get("/nationalistic", (req, res) => {
    //send the url, video-id as parameters
    res.locals.featuresList= params.FEATURE_LIST
    res.render("tagNationalistic.ejs");
    console.log("getting home page");
});

router.get("/location", (req, res) => {
    //send the url, video-id as parameters
    res.render("tagLocation.ejs");
    console.log("getting tagLocation page");
});





module.exports = router;