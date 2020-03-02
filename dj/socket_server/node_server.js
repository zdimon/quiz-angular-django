var http = require('http');
var sockjs = require('sockjs');
var clients = {};
var fs = require("fs");


  var options = {
    key: fs.readFileSync('ssl_key/key.pem', 'utf-8'),
    cert: fs.readFileSync('ssl_key/server.crt', 'utf-8')
};

// Broadcast to all clients
function broadcast(message){
    // iterate through each client in clients object
    for (var client in clients){
      // send the message to that client
      clients[client].write(JSON.stringify(message));
    }
  }

// create sockjs server
var echo = sockjs.createServer();

// on new connection event
echo.on('connection', function(conn) {

  // add this client to clients object
  clients[conn.id] = conn;

  // on receive new data from client event
  conn.on('data', function(message) {
    console.log(message);
    broadcast(JSON.parse(message));
  });

  // on connection close event
  conn.on('close', function() {
    delete clients[conn.id];
  });
  
});

// Create an http server
var server = http.createServer(options);

// Integrate SockJS and listen on /echo
echo.installHandlers(server, {prefix:'/echo'});

// Start server
server.listen(9999, '0.0.0.0');