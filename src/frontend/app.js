var fs = require('fs'),
    express = require('express');
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    _ = require("underscore");

server.listen(8080);


var WatchIO = require('watch.io'),
    watcher = new WatchIO();

watcher.watch('./public/output/images');

app.use(express.static(__dirname + '/public'));
app.get('/', function(req, res) {
   res.sendFile(__dirname + '/index.html');
});

io.on('connection', function (socket) {
    var images = fs.readdirSync('./public/output/images/');

    images = _.filter(images, function(e) {
        return (e != ".DS_Store");
    });

    socket.emit('images', images);

    watcher.on('create', function ( file, stat ) {
        socket.emit('image', file.replace(/^.*[\\\/]/, ''));
    });
});

watcher.close('./data');
