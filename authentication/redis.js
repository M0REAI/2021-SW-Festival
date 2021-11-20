var redis = require('redis');


var redisClient = redis.createClient(6379,'127.0.0.1');
/*
redisClient.auth({password}, function (err) {
    if (err) throw err;
});
*/

redisClient.on('error', function(err) {
    console.log('Redis error: ' + err);
});



module.exports = redisClient;
