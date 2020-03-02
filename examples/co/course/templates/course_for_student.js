var transports = ['websocket', 'xhr-streaming' ,'iframe-eventsource', 'iframe-htmlfile' , 'xhr-polling', 'iframe-xhr-polling', 'jsonp-polling'];
var conn = new SockJS('http://{{ server }}/echo', transports);

var current_user_id = parseInt('{{ request.user.id }}');
var current_user_name = '{{ request.user.user_name }}';

var current_lesson_id = parseInt('{{ lesson.id }}');
var current_user_avatar = '{{ request.user.thumb }}';

function scroolByUlId(id){
var scrH = 0;
    $(id).children('li').each(function () {  
        scrH = scrH + $(this).outerHeight(true);
    }); 
    

    $('#chat_text_messages').stop().animate({
        scrollTop: scrH
    }, 3);

}

	function nl2br( str ) { 
        
        if (str.indexOf("<img class='from_publisher'") == -1){


	      str = str.replace(/([^>])\n/g, '$1<br/>');
          str = str.replace(/ /g, '&nbsp; ');
          //str = '<pre class="prettyprint">'+str+'</pre>'

        } else {

        }
	    return str;
	}



$(document).ready(function(){
                $(".select_all").click(function(event){
                    $("span").slice(1,4).css("background","yellow");
                    event.preventDefault();
                });
            });



conn.onmessage = function(e) {
    var obj = JSON.parse(e.data);
    

    if(obj.act == 'pong') {
        
        alert(obj.message)
    }  

    if(obj.act == 'clear_writeboard') {
        $('#write_board').html('');
        document.getElementById('audio_alert_event').play(); 
    } 

    if(obj.act == 'update_participants') {
        setTimeout(ajaxGet('{% url 'ajax-update-participants' %}', {'lesson_id': "{{lesson.id}}"}, function(content){}),2000)
    }  
 

    if(obj.act == 'text_message') {
        var mess = $('#write_board').html();
        //mess = mess +'<p>'+nl2br(obj.message)+'</p>'; 
        mess = mess +'<p style="font-size: '+obj.text_size+'px; text-align: '+obj.text_align+'; color: '+obj.text_color+' ">'+nl2br(obj.message)+'</p>';
        $('#write_board').html(mess);
       
        var dt = new Date();
        $("#history").append('<li><a href="#">Adding text</a>  '+dt.getHours()+':'+dt.getMinutes()+':'+dt.getSeconds()+'</li>');
        document.getElementById('audio_alert_event').play();
    }  

    if(obj.act == 'chat_message') {

        $("#chat_text_messages").append('<li>'+obj.avatar+' <span> '+obj.message+'</span> <b>'+obj.user_name+'</b></li>');

        scroolByUlId('#chat_text_messages');
        document.getElementById('audio_alert_chat').play(); 
        //infWin(obj.avatar+'<b>'+obj.user_name+'</b><div>'+obj.message+'</div>');
    }  

 
    if(obj.act == 'owner_turn_cam_on') {
       ajaxGet('{% url 'ajax-show-owner-cam' %}', {'lesson_id': current_lesson_id}, function(content){});
    }  

    if(obj.act == 'owner_turn_cam_off') {
       ajaxGet('{% url 'ajax-hide-owner-cam' %}', {'lesson_id': current_lesson_id}, function(content){});
    }  

 if(obj.act == 'turn_student_cam_off') {
      
       $('#student_cam_list').find('#'+obj.token).remove();
   //    ajaxGet('{% url 'ajax-hide-student-cam' %}', {'lesson_id': current_lesson_id, 'user_id': obj.user_id}, function(content){});
   //       $('#participants img').each(function() {
    //    $(this).removeClass('active');
    //});
    } 


    if(obj.act == 'turn_student_mic_off') {
         var id = obj.token+'_mic'
         document[id].JsTurnMicOff();
         $('#'+obj.token+'_mic_off').show();
         $('#'+obj.token+'_mic_on').hide();
      
    } 

    if(obj.act == 'turn_student_mic_on') {
         var id = obj.token+'_mic'
         document[id].JsTurnMicOn();
         $('#'+obj.token+'_mic_on').show();
         $('#'+obj.token+'_mic_off').hide();
      
    } 



    if(obj.act == 'turn_student_cam_out_on') {

       ajaxGet('{% url 'ajax-show-student-cam' type='in' %}', {'lesson_id': current_lesson_id, 'user_id': obj.student_id, 'source': 'lector'}, function(content){});
     
    }

    if(obj.act == 'turn_student_cam_on') {
      
       ajaxGet('{% url 'ajax-show-student-cam' type='out' %}', {'lesson_id': current_lesson_id, 'user_id': obj.user_id, 'source': 'student'}, function(content){});
     // send to all exluding myself
                 $('#participants').children('img').each(function () {  
                    if (parseInt($(this).attr('data-id')) != current_user_id) { 
                    
                    var mess = { "act" : "turn_student_cam_out", 
                                 'lesson_id': current_lesson_id, 
                                 'user_id': $(this).attr('data-id'),   
                                 'student_id': current_user_id,
                                                       
                                };
                   
                    conn.send(JSON.stringify(mess));
                   }
                   

                });  
         $('#participants img#user_participant_'+obj.user_id).addClass('active');

    }  

}
conn.onclose = function() {
    console.log('Disconnected.');
    conn = null;
}
conn.onopen = function() {
    console.log('Connected.');
    mess = {"act" : "open_connect", "user_id" : "{{ request.user.id }}", "lesson_id" : "{{ lesson.id }}" };
    conn.send(JSON.stringify(mess));
}



//////////////////////////////////////
//////////Initialization/////////////
/////////////////////////////////////

    $(document).ready(function(){ 
         
            
             //// Remove video
             $('#student_cam_list').on('click', '.close_student_video', function(e) {
                e.preventDefault();
                $(this).parent().remove();
            });   
            /////////////////////////////////// 



             //// Remove right
             $('#hide_right').on('click', function(e) {
                e.preventDefault();
                
                $('#right_col').hide();
                $('#left_col').removeClass('col-md-9');
                $('#left_col').addClass('col-md-12');
                $('.student_writeboard').attr('style', 'height: 800px');
            });   
            /////////////////////////////////// 

             //// Remove top
             $('#hide_top').on('click', function(e) {
                e.preventDefault();
                
                $('.navbar-fixed-top').hide();
                $('#show_top').show();
            });   
            /////////////////////////////////// 



             //// Test message
             $('#test_message').on('click', function(e) {
                e.preventDefault();
                var message = $(this).attr('data-message');
                var mess = { "act" : "ping", "message" : message };
                conn.send(JSON.stringify(mess));
            });   
            /////////////////////////////////// 

           //setTimeout(ajaxGet('{% url 'ajax-update-participants' %}', {'lesson_id': "{{lesson.id}}"}, function(content){}),2000);
           ajaxGet('{% url 'ajax-update-history' %}', {'lesson_id': "{{lesson.id}}"}, function(content){
             scroolByUlId('#history');
            });
           ajaxGet('{% url 'ajax-update-chat-messages' %}', {'lesson_id': "{{lesson.id}}"}, function(content){
              scroolByUlId('#chat_text_messages');
            });

           {% if lesson.is_camera_on %}
             ajaxGet('{% url 'ajax-show-owner-cam' %}', {'lesson_id': current_lesson_id}, function(content){});
           {% endif %}



             //// Send chat text message
             $('#send_chat_text').on('click', function(e) {
                    e.preventDefault();
                    var link = $(this);
                    $('#participants').children('img').each(function () {  
                    var message = $('textarea#chat_text_input').val(); 
                    var mess = { "act" : "chat_message", 
                                 'content': message, 
                                 'lesson_id': current_lesson_id, 
                                 'avatar': current_user_avatar, 
                                 'user_name': current_user_name,
                                 'user_id': $(this).attr('data-id')                             
                                };
                    conn.send(JSON.stringify(mess));
                });
                    var message = $('textarea#chat_text_input').val();
                   
                    var mess = { "act" : "save_chat_message", 
                                 'message': message, 
                                 'lesson_id': current_lesson_id,
                                 'user_id': current_user_id                            
                                };
                    conn.send(JSON.stringify(mess));
                

              $('textarea#chat_text_input').val('');
              $( "textarea#chat_text_input" ).focus()
               
            });   
            /////////////////////////////////// 


             $('.quick_message').on('click', function(e) {
                //e.preventDefault();
                    var link = $(this);
                    $('#participants').children('img').each(function () {  
                    var message = link.attr('data-message') ;
                    var mess = { "act" : "chat_message", 
                                 'content': message, 
                                 'lesson_id': current_lesson_id, 
                                 'avatar': current_user_avatar, 
                                 'user_name': current_user_name,
                                 'user_id': $(this).attr('data-id')                             
                                };
                    conn.send(JSON.stringify(mess));
                    });
                });


       
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


