require("dotenv").config();
const passport = require('passport');
var redis = require('redis');
client = redis.createClient(6379,'127.0.0.1');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
module.exports = () =>{   

passport.use(new GoogleStrategy({
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: "http://localhost:9000/auth/google/callback"
  },
  function(accessToken, refreshToken, profile, done) {
    done(null, profile);
  }
));

}