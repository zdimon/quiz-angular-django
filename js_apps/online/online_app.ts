import * as $ from "jquery"; 
import * as SockJS from 'sockjs-client';
//var socket_server = document.socket_server;
//
declare var socket_server: any;
declare var user_id: any;


var client =  new SockJS(socket_server);
var message: any;
var users_online: any;


client.onopen = ()=> {
    console.log('open');
    client.send(JSON.stringify({
        "action": "open_connect", 
        "user_id": parseInt(user_id)
    }));
    

};

setTimeout(
    () => {
        $.get('/user_online',(data: any) => {
            users_online = data;
            for(var u in users_online){
                $('#online_users').append('<li>'+users_online[u].username+'</li>');
            }
        });
    }, 2000)

//console.log(socket_server);  