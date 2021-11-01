
//middleware to check if user is logged in, or is admin and so
function ensureAuthenticated(req, res, next){
    console.log("checking if user is auth");
    if(req.isAuthenticated()){
        console.log("user if auth");
        next();
    } else {
        console.log("user is not auth");
        req.flash("info", "You must be logged in to see this page");
        res.redirect("/login");
    }
}


module.exports = {ensureAuthenticated: ensureAuthenticated}