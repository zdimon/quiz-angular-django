//////////////////////////////////////
//////////Initialization/////////////
/////////////////////////////////////

    $(document).ready(function(){
         
               
             $('#take_pic_from_cam').on('click', function(e) {
                var id = $(this).attr('data-id');    
                ajaxGet('/course/ajax/take/pic', {}, function(content){ return false });
            });   
  

               $('#my_cam').on('click', 'a', function(e) {
                var id = $(this).attr('data-id');    
                ajaxGet('/course/ajax/save/pic', {}, function(content){ 

                setTimeout(location.reload(),2000)
                });
            });             


       
     });
