//////////////////////////////////////
//////////Initialization/////////////
/////////////////////////////////////

    $(document).ready(function(){
         
               
             $('#event_list').on('click', 'a.delete_event', function(e) {
                var id = $(this).attr('data-id');    
                ajaxGet('/course/ajax/delete/event', {'id': id}, function(content){});
            });   
  

             $('#event_list').on('click', 'a.move_event_to_incubator', function(e) {
                var id = $(this).attr('data-id');    
                ajaxGet('/course/ajax/move/event/to/incubator', {'id': id}, function(content){});
            }); 


             $('#incubator_list').on('click', 'a.delete_incubator', function(e) {
                var id = $(this).attr('data-id');    
                ajaxGet('/course/ajax/delete/incubator', {'id': id}, function(content){});
            });   
  

             $('#incubator_list').on('click', 'a.move_incubator_to_event', function(e) {
                var id = $(this).attr('data-id');    
                ajaxGet('/course/ajax/move/incubator/to/event', {'id': id}, function(content){});
            }); 

   

             $('#move_all_to_events').on('click', function(e) {
                
                $('.move_incubator_to_event').each(function(i, obj) {
                    $(obj).click();
                });

            }); 


             $('#move_all_to_incubator').on('click', function(e) {
                
                $('.move_event_to_incubator').each(function(i, obj) {
                    $(obj).click();
                });

            }); 

             $('#delete_all_from_events').on('click', function(e) {
                
                $('.delete_event').each(function(i, obj) {
                    $(obj).click();
                });

            }); 


             $('#delete_all_from_incubator').on('click', function(e) {
                
                $('.delete_incubator').each(function(i, obj) {
                    $(obj).click();
                });

            }); 


       
     });
