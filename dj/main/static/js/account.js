function hasUserMedia() {
    return !!(navigator.getUserMedia || navigator.webkitGetUserMedia
    || navigator.mozGetUserMedia || navigator.msGetUserMedia);
    }
    

    function TurnVideo(){

        if (hasUserMedia()) {
        
        navigator.getUserMedia = navigator.getUserMedia ||
        navigator.webkitGetUserMedia || navigator.mozGetUserMedia ||
        navigator.msGetUserMedia;
        
        var constraints = {
        video: {
                mandatory: {
                minWidth: 268,
                minHeight: 200,
                maxWidth: 268,
                maxHeight: 200
                }
            },
            audio: true
            };
        
        
        
        navigator.getUserMedia(constraints, function
        (stream) {
        var video = document.querySelector('video');
        var canvas = document.querySelector('canvas');
        var b = document.querySelector('#b64');
        video.src = window.URL.createObjectURL(stream);
        
        
        }, function (err) {});
        } else {
        alert("Sorry, your browser does not support video.");
        }
    }
    
    function base64ToBlob(base64, mime) 
    {
        mime = mime || '';
        var sliceSize = 1024;
        var byteChars = window.atob(base64);
        var byteArrays = [];
    
        for (var offset = 0, len = byteChars.length; offset < len; offset += sliceSize) {
            var slice = byteChars.slice(offset, offset + sliceSize);
    
            var byteNumbers = new Array(slice.length);
            for (var i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }
    
            var byteArray = new Uint8Array(byteNumbers);
    
            byteArrays.push(byteArray);
        }
    
        return new Blob(byteArrays, {type: mime});
    }

    $('#turn_video').click(function(){
        TurnVideo();
        $('#capture').show();
        $('#video_cam').show();
        $('#turn_video').hide();
        $('#thumb').hide();
    })

    $('#capture').click(function (event) {
        var video = document.querySelector('video');
        var canvas = document.querySelector('canvas');        
        
        canvas.width = video.clientWidth;
        canvas.height = video.clientHeight;
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0);
        
        var cnv = document.getElementsByTagName('canvas')[0];
        var dataUrl = cnv.toDataURL();

        $('#canvas').show();
        $('#video_cam').hide();
        var ui = $('#id_user').val();
        $.post( "/ru/user/save/pic", { data: dataUrl, user_id: ui}, function(){
            location.reload();
        } );

        //console.log(dataUrl);
        //var base64ImageContent = dataUrl.replace(/^data:image\/(png|jpg);base64,/, "");
        //b.innerHTML = base64ToBlob(base64ImageContent, 'image/png');
    })    
    
    
    
    
    