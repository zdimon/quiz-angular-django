import * as SockJS from 'sockjs-client';

export class SocketClient {

    client: any;
    url: string;
    user_id: number = 0;
    username: string = 'guest';
    message_callbacks: Array<(mess: any) => void> = [];

    constructor(url: string, user_id: number, username: string){
        this.url = url;
        this.user_id = user_id;
        this.username = username;
        this.connect();
    }
    
    debug(message: any){
        console.log(message);
    }

    add_message_callback(fun: any){
        this.message_callbacks.push(fun);
    }

    connect(){
        this.client =  new SockJS(this.url);
        this.client.onopen = ()=> {
            //console.log('open');
            //console.dir(this.send_message)
            this.send_message({
                "action": "open_connect", 
                "user_id": this.user_id,
                "username": this.username
            }); 
        };

        this.client.onclose = ()=> {
            //console.log('close');
            this.send_message({
                "action": "close_connect", 
                "user_id": this.user_id
            });
        };

        /// Забрасываем дебажный колбек
        
        this.message_callbacks.push(
            (mess)=>{
                this.debug(mess.data);
            }
        )       


        this.client.onmessage = (mess: any)=> {
            /// Вызываем поочереди колбеки
            var cl = this.message_callbacks.length;
            for (var i = 0; i < cl; i++) {
                this.message_callbacks[i](mess);
            }
        };


    }

    send_message(message: any){
        this.client.send(JSON.stringify(message));
    }




}