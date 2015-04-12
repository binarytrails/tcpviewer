var fs = require('fs'),
    http = require('http'),
    io = require('socket.io'),
    _ = require("underscore");

var WatchIO = require('watch.io'),
    watcher = new WatchIO();

watcher.watch('./data');


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

    watcher.on('create', function ( file, stat ) {
        socket.emit('image', file.replace(/^.*[\\\/]/, ''));
    });
});

watcher.close('./data');
