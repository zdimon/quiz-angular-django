var http = require('http');
var sockjs = require('sockjs');
var redis   = require('redis');
var clients = {};

var settings = require('./config/local')
var request = require('request');

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
    m = JSON.parse(message);
    console.log(m)
    if (m.action == 'open_connect'){
      var room_id = 'channel_'+m.user_id;
      // добавляем идентификатор пользователя в соединение
      conn['user_id'] = m.user_id
      // подписываем на канал редиса
      var browser = redis.createClient();
      browser.subscribe(room_id);
      console.log('user has been described on channel_'+m.user_id);
      browser.on("message", function(channel, message){
        conn.write(message);
      });

      /// Отсылаем всем сообщение что появился новый юзер
      message = {"action": "user_joined", "user_id": m.user_id}
      broadcast(message);      

    }
    /// chat subscription
    if (m.action == 'open_chat_connect'){
      var room_id = 'common_chat';
      var chat_browser = redis.createClient();
      chat_browser.subscribe(room_id);
      chat_browser.on("message", function(channel, message){
        conn.write(message);
      });
      console.log('Chat subscription!!!');
    }

    
  });

  // on connection close event
  conn.on('close', function() {
    message = {"action": "user_left", "user_id": conn.user_id};
    console.log(message);
    broadcast(message);
    delete clients[conn.id];
  });
  
});


function SendOnline() {
  var out = [];
  for (u in clients) {
    out.push(clients[u]['user_id']);
    
  }
  //console.log(out);
  if(out.length>0){
      request.post(
        settings.host+'/socket_online/',
        { json: out },
        function (error, response, body) {
            if (!error && response.statusCode == 200) {
                console.log(body)
            }
        }
    );
  }

}
setInterval(SendOnline, 10000);


// Create an http server
var server = http.createServer();

// Integrate SockJS and listen on /echo
echo.installHandlers(server, {prefix:'/echo'});

// Start server
server.listen(9999, '0.0.0.0');