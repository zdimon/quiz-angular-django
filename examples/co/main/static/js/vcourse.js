//////////////////////////////////////
//////////Initialization/////////////
/////////////////////////////////////

    $(document).ready(function(){
         
               
             $('.test_show').on('click', function(e) {
                var id = $(this).attr('data-id');    
                ajaxGet('/videolearn/ajax/test_show', {}, function(content){ 
                    $("#myModal").modal('show');
                    return false 

                    });
            });   
  

                     
            

       
     });
