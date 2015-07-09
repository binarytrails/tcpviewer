var fs = require('fs'),
    program = require('commander'),
    ip_port_regex = require('ip-port-regex'),
    express = require('express'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    _ = require("underscore"),
    path = require('path');

program
  .version('0.1.0')
  .usage('[options] <file ...>')
  .option('-a, --address <ip:port>', 'listen on the ip address and port', ip_port_regex.v4())
  .parse(process.argv);

server.listen(ip_port_regex.parts(program.address)['port'],
        ip_port_regex.parts(program.address)['ip'],
        function(){
            console.log("Listening on http://%s:%s",
                    server.address().address,
                    server.address().port
            );
        }
);

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
        //console.log(file);
        socket.emit('image', file.replace(/^.*[\\\/]/, ''));
    });

});

watcher.close('./data');
