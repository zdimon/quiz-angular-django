webpackJsonp([2],{803:function(e,n,o){"use strict";Object.defineProperty(n,"__esModule",{value:!0});var i,s=o(323),t=o(306),r=new t(socket_server);r.onopen=function(){console.log("open"),r.send(JSON.stringify({action:"open_connect",user_id:parseInt(user_id)}))},setTimeout(function(){s.get("/user_online",function(e){i=e;for(var n in i)s("#online_users").append("<li>"+i[n].username+"</li>")})},2e3)}},[803]);