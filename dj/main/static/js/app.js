var sock = new SockJS('http://localhost:9999/echo');
sock.onopen = function() {
    console.log('open');
    sock.send(JSON.stringify({"action": "open_connect", "user_id": 1}));
};

sock.onmessage = function(e) {
    alert(e.data)
};

sock.onclose = function() {
    console.log('close');
};

$('#ping').click(function(){

    $.get('/ping');
   
})