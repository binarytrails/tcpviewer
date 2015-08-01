var fs = require('fs'),
    program = require('commander'),
    ip_port_regex = require('ip-port-regex'),
    express = require('express'),
    app = express(),
    server = require('http').Server(app),
    io = require('socket.io')(server),
    _ = require("underscore"),
    path = require('path'),
    readChunk = require('read-chunk'),
    imageType = require('image-type'),
    sqlite = require('sqlite3').verbose();

program
  .version('0.1.0')
  .usage('[options] <file ...>')
  .option('-a, --address <ip:port>', 'listen on the ip address and port', ip_port_regex.v4())
  .option('-d, --database <path>', 'database path')
  .parse(process.argv);

if (!program.address || !program.database)
{
    console.log(program.help());
    process.exit(0);
}

var database = new sqlite.Database(program.database);
    static_dir = "/public",
    images_dir = "/output/images/",
    watched_dir = __dirname + static_dir + images_dir,
    WatchIO = require('watch.io'),
    watcher = new WatchIO({
        delay: 100
    })

function basename(path)
{
   return path.split('/').reverse()[0];
}

function removeElementFromArray(array, element)
{
    var index = array.indexOf(element);
    if (index > -1)
    {
        array.splice(index, 1);
    }
}

function getImages(files, abspath)
{
    images = []
    for (i = 0; i < files.length; i++)
    {
        file = abspath + files[0];
        buffer = readChunk.sync(file, 0, 12);
        if (imageType(buffer))
        {
            images.push(files[i]);
        }
    }
    return images;
}

server.listen(ip_port_regex.parts(program.address)['port'],
        ip_port_regex.parts(program.address)['ip'], function()
        {
            console.log("Listening on http://%s:%s",
                    server.address().address,
                    server.address().port
            );
        }
);

watcher.watch(watched_dir);
app.use(express.static(__dirname + static_dir));

app.get('/', function(req, res)
{
   res.sendFile(__dirname + '/index.html');
});

io.on('connection', function(socket)
{ 
    var images_abspath = __dirname + static_dir + images_dir,
        files = fs.readdirSync(images_abspath),
        images = getImages(files, images_abspath);

    socket.emit('addImages', images, images_dir);
    
    watcher.on('create', function(file)
    {
        images.push(basename(file));
        socket.emit('addImage', basename(file), images_dir);
    }); 
    
    watcher.on('remove', function(file)
    {
        if (images.indexOf(basename(file)) != -1)
        {
            removeElementFromArray(images, basename(file));
            socket.emit('removeImage', basename(file));
            // TODO keep or erase the record from the database?
        }
    });

    socket.on("getData", function(filename)
    { 
        hash = filename.substr(0, filename.lastIndexOf("."));

        var sqlQuery = "SELECT * FROM Images WHERE HASH = '" + hash  + "';";
        sock = this;
        
        data = database.get(sqlQuery, function(error, row)
        {
            sock.emit('setBackData', filename, row);
        });
    });

});

watcher.close(watched_dir);

