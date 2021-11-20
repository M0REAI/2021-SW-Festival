require("dotenv").config();
const passport = require('passport');
const GitHubStrategy = require('passport-naver').Strategy;

module.exports = () => {
passport.use(new GitHubStrategy({
    clientID: process.env.NAVER_CLIENT_ID,
    clientSecret: process.env.NAVER_CLIENT_SECRET,
    callbackURL: "http://localhost:9000/auth/naver/callback"
  }, function(accessToken, refreshToken, profile, done) {
        done(null, profile);
    }));
} 