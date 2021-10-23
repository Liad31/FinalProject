const passport = require("passport");
const LocalStrategy = require("passport-local").Strategy;
const User = require("./models/user");


module.exports = function () {
    //turns a user object into an id
    passport.serializeUser(function (user, done) {
        //serializing the user
        console.log("serializeUser");
        done(null, user._id);
    });
    //turns the id into a user object
    passport.deserializeUser(function (id, done) {
        User.findById(id, function (err, user) {
            console.log("deserializeUser");
            done(err, user);
        });
    });

    passport.use("login", new LocalStrategy({
        usernameField: 'email',
        passwordField: 'psw'
    }, function (email, password, done) {
        console.log("loggin in user, passport");
        User.findOne({ email: email }, function (err, user) {
            if (err) { return done(err); }
            if (!user) {
                return done(null, false, { message: "No user has that Email!" });
            }
            user.checkPassword(password, function (err, isMatch) {
                console.log("checkPassword");
                if (err) { return done(err); }
                if (isMatch) {
                    return done(null, user);
                } else {
                    return done(null, false, { message: "Invalid password" });
                }
            });
        });
    }));
}