const bcyrpt = require("bcryptjs");
const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const SALT_FACTOR = 10;

const userSchema = new Schema({
    username: {type:String, required:true, unique:true},
    password: {type:String, required:true},
    Permissions: {type:Number, default:0},
    createdAt: {type:Date, default:Date.now},
    tags: [{ type: Schema.Types.ObjectId, ref: 'Tag'}]
});

userSchema.pre("save", function(done) {
    var user = this;

    if (!user.isModified("password")) {
        return done();
    }

    console.log("hashing password");
    bcyrpt.genSalt(SALT_FACTOR, function(err, salt) {
        if (err) 
        {
            console.log(`Error: ${err}`);
            return done(err);
        }
        bcyrpt.hash(user.password, salt, function(err, hashPassword) {
            if (err)
            {
                console.log(`Error: ${err}`);
                return done(err);
            }
            user.password = hashPassword;
            done();
        })
    }) 
})

userSchema.methods.checkPassword = function(guess, done) {
    console.log("checking if password is correct");
    if (this.password != null) {
        bcyrpt.compare(guess, this.password, function(err, isMatch) {
            done(err, isMatch);
        });
    }
}

const User = mongoose.model("User", userSchema);

module.exports = User;