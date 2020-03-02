 import * as $ from 'jquery';
 import * as SockJS from 'sockjs-client';
 import {SocketClient} from './socket.client'

 var sc = new SocketClient('http://localhost:9999/echo', 0, 'guest');


