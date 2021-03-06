require("dotenv").config();
const passport = require('passport');
const GitHubStrategy = require('passport-github').Strategy;

module.exports = () => {
passport.use(new GitHubStrategy({
    clientID: process.env.GITHUB_CLIENT_ID,
    clientSecret: process.env.GITHUB_CLIENT_SECRET,
    callbackURL: "http://localhost:9000/auth/github/callback"
  }, function(accessToken, refreshToken, profile, done) {
        done(null, profile);
    }));
} 