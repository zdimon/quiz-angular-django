var transports = ['websocket', 'xhr-streaming' ,'iframe-eventsource', 'iframe-htmlfile' , 'xhr-polling', 'iframe-xhr-polling', 'jsonp-polling'];
var conn = new SockJS('http://{{ server }}/echo', transports);

var current_user_id = parseInt('{{ request.user.id }}');
var current_user_name = '{{ request.user.user_name }}';




	




conn.onmessage = function(e) {
    var obj = JSON.parse(e.data);
    

    if(obj.act == 'lesson_started') {
        
        

        ajaxGet('{% url 'ajax-alert-lesson-started' %}', {'lesson_id': obj.lesson_id}, function(content){
            
            infWin(content.message)      
            document.getElementById('audio_alert').play(); 
            ajaxGet('{% url 'ajax-get-lesson-running' %}', {}, function(content){ });    
        
        });


    }  

   
    if(obj.act == 'lesson_stoped') {
        
       

        ajaxGet('{% url 'ajax-alert-lesson-stoped' %}', {'lesson_id': obj.lesson_id}, function(content){
           infWin(content.message)  
           document.getElementById('audio_alert').play();     
           ajaxGet('{% url 'ajax-get-lesson-running' %}', {}, function(content){ }); 
        });


    }  


   

}

conn.onclose = function() {
    console.log('Disconnected.');
    conn = null;
}

conn.onopen = function() {
    console.log('Connected.');
    mess = {"act" : "open_connect_innerpage", "user_id" : "{{ request.user.id }}" };
    conn.send(JSON.stringify(mess));
}



//////////////////////////////////////
//////////Initialization/////////////
/////////////////////////////////////

    $(document).ready(function(){
         
            
            
         ajaxGet('{% url 'ajax-get-lesson-running' %}', {}, function(content){ });

       
     });



    function infWin(txt) {
        var timer;
        if ($('.informWindows').length) {
            $('.informWindows').addClass('infOut');
            $('.informWindows').stop().fadeOut(400, function() {
                $('.informWindows').first().remove();
            });
        }
        var itm = $('<div>').addClass('informWindows infIn').attr('id', 'informWindows').html('<p>' + txt + '</p>');
        itm.appendTo('body');
        $(document).on('click', '.informWindows', function(event) {
            itm.addClass('infOut');
            itm.fadeOut(400, function() {
                itm.remove();
            });
        });

        clearTimeout(timer);
        timer = setTimeout(function() {
            itm.addClass('infOut');
            itm.fadeOut(400, function() {
                itm.remove();
            });
        }, 30000);
    }


