const bcyrpt = require("bcryptjs");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const SALT_FACTOR = 10;

const userSchema = new Schema({
    email: {type:String, required:true, unique:true},
    password: {type:String, required:true},
    createdAt: {type:Date, default:Date.now},
});

userSchema.pre("save", function(done) {
    var user = this;

    if (!user.isModified("password")) {
        return done();
    }

    bcyrpt.genSalt(SALT_FACTOR, function(err, salt) {
        if (err) {return done(err);}
        bcyrpt.hash(user.password, salt, function(err, hashPassword) {
            if (err) {return done(err);}
            user.password = hashPassword;
            done();
        })
    }) 
})

userSchema.methods.checkPassword = function(guess, done) {
    if (this.password != null) {
        bcyrpt.compare(guess, this.password, function(err, isMatch) {
            done(err, isMatch);
        });
    }
}

const User = mongoose.model("User", userSchema);

module.exports = User;