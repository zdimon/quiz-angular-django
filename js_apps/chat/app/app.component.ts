import { Component, Input, Output, ElementRef, ViewChild} from '@angular/core';
import * as $ from "jquery"; 
import { ChatService } from './http.service'; 
import { SocketService } from './socket.service';
import { WindowRefService } from './window.service'
//console.log(QuizeService);

@Component({
    selector: 'chat-app',
    templateUrl: 'chat.html'
    
})
export class AppComponent { 
   
    socket_server: string = $("chat-app").attr('data-socket-server');
    user_id : string = $("chat-app").attr('data-user-id');
    is_authenticated: string = $("chat-app").attr('data-is-authenticated');
    user_name: string = $("chat-app").attr('data-user-name'); 
    language: string = $("chat-app").attr('data-language');
    guest_name: string = 'guest';   
    i18n: any = {};
    text_message: string;
    messages: any =[];
    subscription: any;
    show_next: boolean = true;
    lang_ru: boolean = false;
    lang_en: boolean = false;
    window: any;
    @ViewChild('scrollMe') private myScrollContainer: ElementRef;
    @ViewChild('inputBox') private inputBox: ElementRef;

    constructor(
        private socket_service: SocketService, 
        private _http: ChatService,
        private _window: WindowRefService
    ) { 
        this.window = _window.nativeWindow;
        if (this.language == 'ru') {
            this.lang_ru = true;
        } else {
            this.lang_en = true;
        }
    }

    ngOnInit() {
        // get I18n messages
        this._http.init(this.language);
        
        this._http.getI18n(this.language).subscribe((data: any) => {
            this.i18n = data;
            
        });

        // get chat messages
        this._http.getMessages().subscribe((data: any) => {
            this.messages = data.data;
        });

        this.socket_service.init(this.socket_server);
        this.subscription = this.socket_service.getEmmiter()
        .subscribe((mes: any) => { 
            if (mes.action == 'add_message') {
                this.messages.push(mes.data);
            }
        });

    }

    submit(): void{
        let obj = {"message": this.text_message}
        if(this.is_authenticated=='true'){
            obj['username'] = this.user_name;
        } else {
            obj['username'] = this.guest_name;
        }
        this._http.saveMessage(obj).subscribe((data: any) => {
            this.text_message = '';
        });
    }    

    keyPressHandler(code: number) {
        
       
        if (code === 13){
            this.submit();
        }
    }
    
    /*
        Scrolling chat box.
    */

   ngAfterViewChecked() {
        this.scrollToBottom();
    }

    private scrollToBottom(): void {
        try {
            this.myScrollContainer.nativeElement.scrollTop = this.myScrollContainer.nativeElement.scrollHeight;
        } catch(err) { }
    }
    
    /*
        get next question
    */
   nextQuestion(){
    this._http.nextQuestion().subscribe(
        (data: any) => {
            console.log(data);
            this.show_next = false;
            this.text_message = '';
        }   
    );

}    

    toggleLang(lang: string){
        if(lang=='ru'){
            this.lang_ru = !this.lang_ru;
            if(!this.lang_ru && !this.lang_en) {
                this.lang_en = true;
            }
        } 
        if(lang == 'en'){
            this.lang_en = !this.lang_en;
            if(!this.lang_ru && !this.lang_en) {
                this.lang_ru = true;
            }
        }
    }


}