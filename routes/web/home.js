const router = require("express").Router();
const passport = require("passport");
const User = require("../../models/user");


router.get("/login", (req, res) => {
    res.render("login.ejs");
    console.log("getting login page");
})

router.post("/login", (req, res, next) => {
    console.log("logging in");
    next();
}
 ,passport.authenticate("login", {
    successRedirect: "/",
    failureRedirect: "/login",
    failureFlash: true
}));

router.get("/logout", function(req, res) {
    console.log("logging out");
    req.logout();
    res.redirect("/")
});

router.get("/signup", (req, res) => {
    res.render("signup.ejs");
    console.log("getting signup page");
})

// router.post("/sign", (req, res) => {
//     let email = console.log(req.body.email)
//     let psw = console.log(req.body.psw)
//     let psw_repeat = console.log(req.body.psw_repeat)
// });

router.get("/", (req, res) => {
    //send the url, video-id as parameters
    res.render("home.ejs");
    console.log("getting home page");
});

router.post("/signup", function (req, res, next) {
    let email = req.body.email;
    let password = req.body.psw;
    let re_password = req.body.psw_repeat;
    console.log("trying to sign up user");
    console.log("checking if mail already in use");
    User.findOne({ email: email }, function (err, user) {
        if (err)
         { 
            console.log(`Error: ${err}`);
            return next(err);
         }
        if (user) {
            req.flash("error", "There is already an account with that email");
            console.log("email user is taken, redirecting to login");
            return res.redirect("/login");
        }
        if (password != re_password) {
            req.flash("error", "passwords does not match");
            console.log("passwords does not match");
            return res.redirect("/signup");
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