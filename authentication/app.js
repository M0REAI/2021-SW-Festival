require("dotenv").config();

var redis = require('./redis');
const express = require('express')
const passport = require('passport');
const google = require('./passport/googleStrategy')
const github = require('./passport/githubStrategy')
const naver = require('./passport/naverStrategy')
const session = require('express-session');
var RedisStore = require('connect-redis')(session);

var JSON = require('JSON');

var app = express()

google()
github()
naver()


app.use(express.json());
app.use(session({
   store: new RedisStore({
        client: redis,
        host: 'localhost',
        port: 6379,
        prefix : "session:",
        db : 0,
        saveUninitialized: false,
        resave: false

    }),

    secret: process.env.SECRET_CODE,
    cookie: { maxAge: 60 * 60 * 1000 },
    //resave: true,
    //saveUninitialized: false
  }));

app.use(passport.initialize()); 
app.use(passport.session());



passport.serializeUser((user, done) => {
    done(null, user); // user객체가 deserializeUser로 전달됨.
  });
passport.deserializeUser((user, done) => {
    done(null, user); // 여기의 user가 req.user가 됨
});

const authenticateUser = (req, res, next) => {
    if (req.isAuthenticated()) {
      next();
    } else {
      res.status(301).redirect('/auth');
    }
  };

app.get('/', authenticateUser, (req, res, next) => {
    
    if(req.session.user){
        res.send({"사용자 이름" : req.session.user.name,"제공자 ":req.session.user.provider})
    }
    else{
        res.send({ 'title': 'Express','user':'로그인을 해주세요'});
    }
    
});

app.get('/auth', (req, res, next)  => {
    res.send({ title: 'Login Page' })
});

app.get('/auth/google',
  passport.authenticate('google', { scope: ['profile'] })
);

app.get('/auth/github',
  passport.authenticate('github'),
);

app.get('/auth/naver',
  passport.authenticate('naver'),
);

app.get('/auth/google/callback',
	passport.authenticate('google', {
    failureRedirect: '/auth'}),
    (req,res)=>{
        console.log(req.user)
        req.session.user = {
            id: req.user.id,
            name: req.user.displayName,
            provider : req.user.provider
        }
        res.redirect('/')
    }
);

app.get('/auth/github/callback',
	passport.authenticate('github', {
  	failureRedirect: '/auth',
}), (req,res)=>{
    console.log(req.user)
    req.session.user = {
        id: req.user.id,
        name: req.user.displayName,
        provider : req.user.provider
    }
    res.redirect('/')
});

app.get('/auth/naver/callback',
	passport.authenticate('naver', {
  	failureRedirect: '/auth',
}), (req,res)=>{
    console.log(req.user.emails[0].value)
    req.session.user = {
        id: req.user.emails[0].value,
        name: req.user.displayName,
        provider : req.user.provider
    }
    res.redirect('/')
});

app.get('/auth/logout', function(req, res){    
    if(req.session.user){
        console.log('로그아웃');
        
        req.session.destroy(function(err){
            if(err) throw err;
            console.log('세션 삭제하고 로그아웃됨');
            res.redirect('/auth');
        });
    }
    else{
        console.log('로그인 상태 아님');
        res.redirect('/auth');
    }
});

app.get('/auth/userinfo', (req, res, next) => {
    
    if(req.session.user){
        res.send({"사용자 이름" : req.session.user.name,"제공자 ":req.session.user.provider})
    }
    else{
        res.send({ 'title': 'Express','user':'로그인을 해주세요'});
    }
    
});
app.listen('9000',()=>{
    console.log('listening in port 9000!')
})
