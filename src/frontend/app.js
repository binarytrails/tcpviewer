var fs = require('fs')
    , http = require('http')
    , socketio = require('socket.io');

var _ = require("underscore");

var server = http.createServer(function(req, res) {
    res.writeHead(200, { 'Content-type': 'text/html'});
    res.end(fs.readFileSync(__dirname + '/index.html'));
}).listen(8080, function() {
    console.log('Listening at: http://localhost:8080');
});

var images = fs.readdirSync('./data/');

images = _.filter(images, function(e) {
    return (e != ".DS_Store");
});

console.log(images);

socketio.listen(server).on('connection', function (socket) {
    socket.on('message', function (msg) {
        console.log('Message Received: ', msg);
        socket.broadcast.emit('message', msg);
    });
});