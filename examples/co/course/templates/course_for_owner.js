var transports = ['websocket', 'xhr-streaming' ,'iframe-eventsource', 'iframe-htmlfile' , 'xhr-polling', 'iframe-xhr-polling', 'jsonp-polling'];
var conn = new SockJS('http://{{ server }}/echo', transports);

var current_user_id = parseInt('{{ request.user.id }}');
var current_user_name = parseInt('{{ request.user.username }}');
var current_lesson_id = parseInt('{{ lesson.id }}');
var current_user_name = '{{ request.user.user_name }}';
var current_user_avatar = '{{ request.user.thumb }}';

var is_cam_on = '{{ request.user.is_cam_on }}'
var is_mic_on = '{{ request.user.is_mic_on }}'


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


conn.onmessage = function(e) {
    var obj = JSON.parse(e.data);
    

    if(obj.act == 'pong') {
        
        alert(obj.message)
    }  
 
    if(obj.act == 'chat_message') {
      
        $("#chat_text_messages").append('<li>'+obj.avatar+' <span> '+obj.message+'</span> <b>'+obj.user_name+'</b></li>')
    scroolByUlId('#chat_text_messages');
       infWin(obj.avatar+'<b>'+obj.user_name+'</b><div>'+obj.message+'</div>');
       document.getElementById('audio_alert_chat').play(); 

    }  


    if(obj.act == 'clear_writeboard') {
        $('#write_board').html('');
        document.getElementById('audio_alert_event').play(); 
    }  

    if(obj.act == 'add_image_from_publisher') {
    
        $('#from_publisher').prepend(obj.image)
        if(obj.publish == 'yes') {

          $('#uploaded_image_'+obj.image_id).click();
          
        }
    } 

    if(obj.act == 'turn_student_cam_out_on') {

       ajaxGet('{% url 'ajax-show-student-cam' type='in' %}', {'lesson_id': current_lesson_id, 'user_id': obj.student_id, 'source': 'lector'}, function(content){});
     
    }  


    if(obj.act == 'turn_student_cam_off') {

       ajaxGet('{% url 'ajax-hide-student-cam' %}', {'lesson_id': current_lesson_id, 'user_id': obj.user_id}, function(content){});
          $('#participants img').each(function() {
        //$(this).removeClass('active');
    });
    } 






    if(obj.act == 'text_message') {
     
        var mess = $('#write_board').html();
        mess = mess +'<p style="font-size: '+obj.text_size+'px; text-align: '+obj.text_align+'; color: '+obj.text_color+' ">'+nl2br(obj.message)+'</p>';
        $('#write_board').html(mess);
       
        ///Prism.highlightAll();
        
        
        var dt = new Date();
        $("#history").append('<li><a href="#">Adding text</a>  '+dt.getHours()+':'+dt.getMinutes()+':'+dt.getSeconds()+'</li>')
         //$('code').each(function(i, block) {
         //   hljs.highlightBlock(block);
         // });
        document.getElementById('audio_alert_event').play();
 
        
    }  

    if(obj.act == 'update_participants') {
        ajaxGet('{% url 'ajax-update-participants' %}', {'lesson_id': "{{lesson.id}}"}, function(content){});
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


             $('#incubator_list').on('click', 'a', function(e) {
                var id = $(this).attr('data-id');    
                ajaxGet('/course/ajax/incubator/fire', {'id': id}, function(content){});
                $(this).html('<span class="glyphicon glyphicon-ok"></span>'+$(this).html()); 
            });   
            

             ajaxGet('{% url 'ajax-update-participants' %}', {'lesson_id': "{{lesson.id}}"}, function(content){});
             ajaxGet('{% url 'ajax-update-history' %}', {'lesson_id': "{{lesson.id}}"}, function(content){
                scroolByUlId('#history');
             });
             ajaxGet('{% url 'ajax-update-chat-messages' %}', {'lesson_id': "{{lesson.id}}"}, function(content){
              scroolByUlId('#chat_text_messages');
             });
             //// Test message
             $('#test_message').on('click', function(e) {
                e.preventDefault();
                var message = $(this).attr('data-message');
                var mess = { "act" : "ping", "message" : message };
                conn.send(JSON.stringify(mess));
            });   
            /////////////////////////////////// 

             //// Turn cam on
             $('#turn_owner_cam_on').on('click', function(e) {
                e.preventDefault();
                $(this).hide()
                $('#turn_owner_cam_off').show();
                ajaxGet('{% url 'ajax-turn-owner-cam-on' %}', {'lesson_id': current_lesson_id}, function(content){});
            });   
            /////////////////////////////////// 



            ////Start/stop lesson
             $('#start_lesson_btn').on('click', function(e) {
                $(this).hide()
                $('#stop_lesson_btn').show();
                ajaxGet('{% url 'ajax-start-lesson' %}', {'lesson_id': current_lesson_id}, function(content){});
            });   
             $('#stop_lesson_btn').on('click', function(e) {
                $(this).hide()
                $('#start_lesson_btn').show();
                ajaxGet('{% url 'ajax-stop-lesson' %}', {'lesson_id': current_lesson_id}, function(content){});
            });  
            /////////////////////////////////// 



            //*********CAMERA*******************

            //// Turn cam off
             $('#turn_owner_cam_off').on('click', function(e) {
                $(this).hide()
                $('#turn_owner_cam_on').show();
                ajaxGet('{% url 'ajax-turn-owner-cam-off' %}', {'lesson_id': current_lesson_id}, function(content){});
            });   
            /////////////////////////////////// 

            if(is_cam_on=='True'){
              $('#turn_owner_cam_on').click();

                if(is_mic_on=='True'){
                  setTimeout($('#turn_owner_mic_on').click(),3000);
                }


            }

             //// Turn mic of
             $('#turn_owner_mic_off').on('click', function(e) {
                e.preventDefault();
                $(this).hide()
                $('#turn_owner_mic_on').show();
                document["owner_cam_obj"].JsTurnMicOff();
            });   
            /////////////////////////////////// 

             //// Turn mic on
             $('#turn_owner_mic_on').on('click', function(e) {
                e.preventDefault();
                $(this).hide()
                $('#turn_owner_mic_off').show();
                document["owner_cam_obj"].JsTurnMicOn();
            });   
            ///////////////////////////////////



            // Students mic ++++++++++++++++++++++++++++++

             //// Turn mic of
             $('#student_cam_list').on('click', '.turn_student_mic_on', function(e) {
                e.preventDefault();
                $(this).hide();
                $(this).next().show();

                var mess = { "act" : "turn_student_mic_on", 'lesson_id': current_lesson_id, 'token': $(this).attr('data-token'), 'user_id': $(this).attr('data-id') };
                conn.send(JSON.stringify(mess));

            });   
            /////////////////////////////////// 

             //// Turn mic on
            $('#student_cam_list').on('click', '.turn_student_mic_off', function(e) {
                e.preventDefault();
                $(this).hide()
                $(this).prev().show();
                var mess = { "act" : "turn_student_mic_off", 'lesson_id': current_lesson_id, 'token': $(this).attr('data-token'), 'user_id': $(this).attr('data-id') };
                conn.send(JSON.stringify(mess));
            });   
            ///////////////////////////////////



             //// Test message
             $('#student_cam_list').on('click', '.turn_student_cam_off_button', function(e) {
                var token = $(this).attr('data-token');
                
                e.preventDefault();
                 $('#participants').children('img').each(function () {  
                                       
                   var mess = { "act" : "turn_student_cam_off", 'lesson_id': current_lesson_id, 'token': token, 'user_id': $(this).attr('data-id') };
                   conn.send(JSON.stringify(mess));
                   

                });  
                
                $(this).parent().remove();
 


            });   


            /////////////////////////////////// 

           

             //// Turn mic of
             $('#turn_owner_mic_off').on('click', function(e) {
                e.preventDefault();
                document["owner_cam_obj"].JsTurnMicOff();
            });   
            /////////////////////////////////// 

             //// Turn mic on
             $('#turn_owner_mic_on').on('click', function(e) {
                e.preventDefault();
                document["owner_cam_obj"].JsTurnMicOn();
            });   
            /////////////////////////////////// 




             //// Turn cam off
             $('#clear_writeboard').on('click', function(e) {
                //e.preventDefault();

                    $('#participants').children('img').each(function () {
                    var mess = { "act" : "clear_writeboard", 'lesson_id': current_lesson_id, 'user_id': $(this).attr('data-id')};
                    conn.send(JSON.stringify(mess));
                });


                //ajaxGet('{% url 'ajax-turn-owner-cam-off' %}', {'lesson_id': current_lesson_id}, function(content){});
            });   
            /////////////////////////////////// 



             //// Send text message
             $('.send_text').on('click', function(e) {
                //e.preventDefault();
                    var link = $(this);
                    var text_size = $('#text_size').val();
                    var text_color = $('#text_color').val();
                    var text_align = $('#text_align').val();
                    $('#participants').children('img').each(function () {  
                    var message = $('textarea#text_lesson').val(); 
                    var mess = { "act" : "text_message", 
                                 'content': message, 
                                 'lesson_id': current_lesson_id, 
                                 'user_id': $(this).attr('data-id'),
                                 'text_size': text_size,
                                 'text_color': text_color,
                                 'text_align': text_align,
                                 'replace': link.attr('data-replace')                              
                                };
                    conn.send(JSON.stringify(mess));
                });
                    var message = $('textarea#text_lesson').val();

                    
                    if(link.attr('data-replace')=='yes') {
                        var tp = 'text_replace';                    
                    } else {
                        var tp = 'text_add';    
                    }
                    var mess = { "act" : "save_event", 
                                 'message': message, 
                                 'text_size': text_size,
                                 'text_color': text_color,
                                 'text_align': text_align,
                                 'type': tp                              
                                };
                    conn.send(JSON.stringify(mess));

              $('textarea#text_lesson').val('');
              $( "textarea#text_lesson" ).focus()
               
            });   
            /////////////////////////////////// 


             //// Send image
             $('.div_uploaded_img').on('click', 'a', function(e) {
                //e.preventDefault();
       
                    var link = $(this);
                    var lesson_id = link.attr('data-lesson') 
                    var image_path = link.attr('data-filename') 
                    var image_id = link.attr('data-filename') 
                    $('#participants').children('img').each(function () {  
                    var message = $('textarea#text_lesson').val(); 
                    var mess = { "act" : "send_image", 
                                 'image_path': image_path, 
                                 'lesson_id': current_lesson_id, 
                                 'user_id': $(this).attr('data-id'),
                                 'replace': link.attr('data-replace')                              
                                };
                    conn.send(JSON.stringify(mess));
                    
                });

                    var mess = { "act" : "save_event", 
                                 'message': image_path, 
                                 'type': 'image_file'                              
                                };
                    conn.send(JSON.stringify(mess));

                   $(this).remove();
               
            });   
            /////////////////////////////////// 



            //// Turn students camera
             $('#participants').on('click', 'img', function(e) {
                //e.preventDefault();
       
                    var link = $(this);
                    var user_id = link.attr('data-id') 
                   
                    var mess = { "act" : "turn_student_camera", 
                                 'user_id': user_id,         
                                 'lesson_id': current_lesson_id                            
                               };
    
                    conn.send(JSON.stringify(mess));

                   $('#participants img').each(function() {
                        $(this).removeClass('active');
                    });
                   $(this).addClass('active');
               
            });   
            /////////////////////////////////// 


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


