const router = require("express").Router();
const passport = require("passport");
const User = require("../../models/user");
const params = require("../../params/params");
// const VideoModule = require("../../models/video");
// const Video=VideoModule.Video
// const ExpertVideos=VideoModule.ExpertVideos
const ensureAuthenticated = require("../../auth/auth").ensureAuthenticated;
const Img = require("../../models/israelTag")


router.get("/login", (req, res) => {
    if (!req.isAuthenticated()) {
    res.render("login.ejs");
    } else {
        req.flash("info", "You are already logged in!");
        res.redirect("/");
    }
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


router.post("/signup", function (req, res, next) {
    let username = req.body.username;
    let password = req.body.password;
    let re_password = req.body.repassword;
    console.log("trying to sign up user", username);
    console.log("checking if mail already in use");
    User.findOne({ username: username }, function (err, user) {
        if (err)
         { 
            console.log(`Error: ${err}`);
            return next(err);
         }
        if (user) {
            req.flash("error", "There is already an account with that username");
            console.log("username is taken, redirecting to login");
            return res.redirect("/login");
        }
        if (username.length < 6  || password.length < 6) {
            req.flash("error", "username and password must be at least 6 chars long");
            console.log("pasusername or password in bad format");
            return res.redirect("/signup");
        }
        if (password != re_password) {
            req.flash("error", "passwords does not match");
            console.log("passwords does not match");
            return res.redirect("/signup");
        }
        console.log("creating user");
        let newUser = User({
            username: username,
            password: password
        });
        newUser.save(next);
    });
}, passport.authenticate("login", {
    successRedirect: "/",
    failureRedirect: "/signup",
    failureFlash: true
}));

router.get("/", ensureAuthenticated,(req, res) => {
    res.locals.featuresList= params.FEATURE_LIST   
    res.render("home.ejs");
    console.log("getting home page");
});

router.get("/data",ensureAuthenticated,(req, res) => {
    if(req.user.Permissions < 2){
        req.flash("error", "you dont have the pernissions for this page");
        console.log("dont have the pernissions for this page");
        return res.status(404)
    }
    res.render("data.ejs");
})
router.post("/submitTag", (req,res) => {
    console.log(req.religiosity, "religiosity")
})

router.get("/nationalistic", ensureAuthenticated,(req, res) => {
    //send the url, video-id as parameters
    res.locals.featuresList= params.FEATURE_LIST
    res.render("tagNationalistic.ejs");
    console.log("getting home page");
});

router.get("/location", ensureAuthenticated, (req, res) => {
    //send the url, video-id as parameters
    res.render("tagLocation.ejs");
    console.log("getting tagLocation page");
});

async function getImage(){
    let filter = {
        "tagged": false,
    }
    let options = {}

    return await Img.findOne(filter, null, options, function (err, image) {
        if (err) {
            console.log(err)
            return
        }
        if (!image) {
            console.log("no image found")
            throw new Error("no image found")   
        }
        else {
            return image.id;
        }
    }).clone().catch((err)=>{
        console.log(err);
        return 0;})
}

router.get("/israel", ensureAuthenticated, async (req, res) => {
    //send the url, video-id as parameters
    try {
        id = await getImage();
        console.log("image is:" + String(id));
        res.locals.imageID = "images/" + id['id'] + ".png";
    } catch {
        res.locals.imageID = "images/" + "0" + ".png";
        res.render("israel.ejs");
    }
    res.render("israel.ejs");
    console.log("getting israelTag page");

});



module.exports = router;