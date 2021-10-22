const router = require("express").Router();

router.get("/", (req, res) => {
    res.render("logIn.ejs");
})

router.get("/signUp", (req, res) => {
    res.render("signUp.ejs");
})

router.post("/sign", (req, res) => {
    let email = console.log(req.body.email)
    let psw = console.log(req.body.psw)
    let psw_repeat = console.log(req.body.psw_repeat)

});

router.get("/home", (req, res) => {
    //send the url, video-id as parameters
    res.render("home.ejs");
});

module.exports = router;