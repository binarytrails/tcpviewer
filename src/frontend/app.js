var fs = require('fs'),
    express = require('express');
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    _ = require("underscore"),
    path = require('path');

server.listen(8080);


var WatchIO = require('watch.io'),
    watcher = new WatchIO({
        delay: 100
    });

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

    watcher.on('change', function ( type, file, stat ) {
        console.log(file);
        socket.emit('image', file.replace(/^.*[\\\/]/, ''));
    });

});

watcher.close('./data');
