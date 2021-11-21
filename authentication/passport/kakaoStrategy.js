require("dotenv").config();
const passport = require('passport');
const GitHubStrategy = require('passport-kakao').Strategy;

module.exports = () => {
passport.use(new GitHubStrategy({
    clientID: process.env.KAKAO_CLIENT_ID,
    clientSecret: process.env.KAKAO_CLIENT_SECRET,
    callbackURL: "http://localhost:9000/auth/kakao/callback"
  }, function(accessToken, refreshToken, profile, done) {
        done(null, profile);
    }));
} 