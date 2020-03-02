var transports = ['websocket', 'xhr-streaming' ,'iframe-eventsource', 'iframe-htmlfile' , 'xhr-polling', 'iframe-xhr-polling', 'jsonp-polling'];
var conn = new SockJS('{{ hostname }}/echo', transports);

var current_user_id = parseInt('{{ user_id }}');


conn.onmessage = function(e) {
    var obj = JSON.parse(e.data);
    

    if(obj.act == 'send_message') {
        
        alert('I have got the message!')
    }  
 

}
conn.onclose = function() {
    console.log('Disconnected.');
    conn = null;
}
conn.onopen = function() {
    console.log('Connected.');
    mess = {"act" : "open_connect", "user_id" : "{{ user_id }}", "auth" : "true", "room_id" : "{{ room_id }}", "place" : "chat" };
    conn.send(JSON.stringify(mess));
}



//////////////////////////////////////
//////////Initialization/////////////
/////////////////////////////////////

    $(document).ready(function(){
         
            
       
     });




