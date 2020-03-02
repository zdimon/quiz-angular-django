function hasUserMedia() {
    return !!(navigator.getUserMedia || navigator.webkitGetUserMedia
    || navigator.mozGetUserMedia || navigator.msGetUserMedia);
    }
    
    if (hasUserMedia()) {
    
    navigator.getUserMedia = navigator.getUserMedia ||
    navigator.webkitGetUserMedia || navigator.mozGetUserMedia ||
    navigator.msGetUserMedia;
    
    var constraints = {
    video: {
            mandatory: {
            minWidth: 480,
            minHeight: 320,
            maxWidth: 1024,
            maxHeight: 768
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
    
    
    
    document.querySelector('#capture').addEventListener('click',
    function (event) {
    
        canvas.width = video.clientWidth;
        canvas.height = video.clientHeight;
        var context = canvas.getContext('2d');
        context.drawImage(video, 0, 0);
        
        var cnv = document.getElementsByTagName('canvas')[0];
        var dataUrl = cnv.toDataURL();
        console.log(dataUrl);
        var base64ImageContent = dataUrl.replace(/^data:image\/(png|jpg);base64,/, "");
        b.innerHTML = base64ToBlob(base64ImageContent, 'image/png');
    });
    
    }, function (err) {});
    } else {
    alert("Sorry, your browser does not support video.");
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
    
    
    
    
    