const passport = require("passport");
const LocalStrategy = require("passport-local").Strategy;
const User = require("./models/user");


module.exports = function () {
    //turns a user object into an id
    passport.serializeUser(function (user, done) {
        //serializing the user
        console.log("serializing User");
        done(null, user._id);
    });
    //turns the id into a user object
    passport.deserializeUser(function (id, done) {
        User.findById(id, function (err, user) {
            console.log("deserializing User");
            done(err, user);
        });
    });

    passport.use("login", new LocalStrategy({
        usernameField: 'email',
        passwordField: 'psw'
    }, function (email, password, done) {
        console.log("logging in user, passport");
        User.findOne({ email: email }, function (err, user) {
            if (err) {
                console.log(`Error: ${err}`);
                return done(err);
            }
            if (!user) {
                return done(null, false, { message: "no user has that Email!" }); //the message will be flashed
            }
            user.checkPassword(password, function (err, isMatch) {
                console.log("checkPassword");
                if (err) {
                    console.log(`Error: ${err}`);
                    return done(err);
                }
                if (isMatch) {
                    return done(null, user);
                } else {
                    return done(null, false, { message: "Invalid password" }); //the message will be flashed
                }
            });
        });
    }));
}