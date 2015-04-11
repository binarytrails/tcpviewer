var fs = require('fs'),
    http = require('http'),
    io = require('socket.io'),
    _ = require("underscore"),
    watch = require('watch');

var server = http.createServer(function(req, res) {
    res.writeHead(200, { 'Content-type': 'text/html'});
    res.end(fs.readFileSync(__dirname + '/index.html'));
}).listen(8080, function() {
    console.log('Listening at: http://localhost:8080');
});


io.listen(server).on('connection', function (socket) {
    var images = fs.readdirSync('./data/');

    images = _.filter(images, function(e) {
        return (e != ".DS_Store");
    });


    socket.emit('images', images);

    socket.on('image', function (img) {
        console.log('Image Received: ', img);
        socket.broadcast.emit('image', img);
    });
});