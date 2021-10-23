const router = require("express").Router();
const passport = require("passport");
const User = require("../../models/user");


router.get("/login", (req, res) => {
    res.render("login.ejs");
    console.log("getting login");
})

router.post("/login", passport.authenticate("login", {
    successRedirect: "/",
    failureRedirect: "/login",
    failureFlash: true
}));

router.get("/logout", function(req, res) {
    req.logout();
    res.redirect("/")
});

router.get("/signup", (req, res) => {
    res.render("signup.ejs");
    console.log("getting signup");
})

router.post("/sign", (req, res) => {
    let email = console.log(req.body.email)
    let psw = console.log(req.body.psw)
    let psw_repeat = console.log(req.body.psw_repeat)

});

router.get("/", (req, res) => {
    //send the url, video-id as parameters
    res.render("home.ejs");
    console.log("getting home");
});

router.post("/signup", function (req, res, next) {
    let email = req.body.email;
    let password = req.body.psw;
    let re_password = req.body.psw_repeat;
    console.log("signing up user");
    console.log(req.body);

    User.findOne({ email: email }, function (err, user) {
        if (err) { return next(err); }
        if (user) {
            req.flash("error", "There is already an account with that email");
            console.log("email user is taken, redirecting to login");
            return res.redirect("/login");
        }
        console.log("creating user");
        var newUser = User({
            email: email,
            password: password
        });
        newUser.save(next);
    });
}, passport.authenticate("login", {
    successRedirect: "/",
    failureRedirect: "/signup",
    failureFlash: true
}));

module.exports = router;