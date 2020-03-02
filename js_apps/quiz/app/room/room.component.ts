import { Component, Input, Output, ElementRef, ViewChild} from '@angular/core';
import { SocketService } from '../utils';  
import { QuizeService } from '../http.service'; 
import { ArraySortPipe } from '../pipes'
import {ActivatedRoute, Router} from '@angular/router';
import { WindowRefService } from '../utils'

import * as $ from "jquery"; 
//console.log(QuizeService);

@Component({
    selector: 'quiz-app',
    templateUrl: 'room.html'
    
})
export class RoomComponent { 
    window: any;
    room_token : string;
    socket_server: string = $("quiz-app").attr('data-socket-server');
    user_id: number = parseInt($("quiz-app").attr('data-user-id'));
    client: any;
    room: any = {'users': []};
    subscription: any;
    winner: any;
    message: any = {};
    text_message: string;
    show_next: boolean = true;
    is_first_question: boolean = true;
    is_done: boolean = false;
    i18n: any = {};
    csrf_token: string;
    language: string;
    lang_ru: boolean = false;
    lang_en: boolean = false;
    @ViewChild('scrollMe') private myScrollContainer: ElementRef;
    @ViewChild('inputBox') private inputBox: ElementRef;

   
    
    constructor(
        private socket_service: SocketService, 
        private _http: QuizeService,
        private route:ActivatedRoute,
        private _window: WindowRefService
    ) { 
        this.window = _window.nativeWindow;
        if (this.window.current_language == 'ru') {
            this.lang_ru = true;
        } else {
            this.lang_en = true;
        }
    }



    ngOnInit() {
        // get I18n messages
        this.room_token = this.route.snapshot.params['token'];
        localStorage.setItem('current_token', this.room_token); 
        this._http.getI18n().subscribe((data: any) => {
            this.i18n = data;
        });

        /*
           подключаемся к сокет серверу и подписываемся на событие прихода сообщения
           это событие генерит эмитер сокет сервиса
        */
        this.socket_service.init(this.socket_server, this.user_id, 'guest');
        this.subscription = this.socket_service.getEmmiter()
        .subscribe((mes: any) => { 
            this.message = mes;

            if (mes.action == 'add_message') {
                this.room.messages.push(mes.data);
            }

            if (mes.action == 'update_users') {
                this.room.users = mes.users;
            }

            if (mes.action == 'update_question') {
                
                this.getQuestion();
               
            }

            if (mes.action == 'admin_message') {
                
                setTimeout(()=>{    
                    this.room.messages.push(
                        {
                            "user": {"avatar": "/static/image/admin.png"},
                            "text": mes.message,
                            "question_ru": mes.question_ru,
                            "question_en": mes.question_en,
                            "is_right": "alert"
                        }
                    );
               },mes.timer);


            }

            if (mes.action == 'user_joined') {
                this._http.getUserInfo(this.room_token,mes.user_id).subscribe(
                    (data: any)=>{
                        this.addUser(data.user);
                    }
                );
            }

            if (mes.action == 'end_quiz') {
                this.endQuiz();
            }            

            if (mes.action == 'user_left') {
                this.removeUser(mes.user_id);
            }

        });        
       
        /*
            запрашиваем информацию о текущей комнате
        */   
        this._http.getRoomInfo(this.room_token).subscribe((data: any)=>{
                this.room = data;
                this.csrf_token = data.token
                // if room is compleated take the winner
                if(this.room.is_done){
                    this.endQuiz();
                }
            }
        )
        
        /*
            подключаемся к комнате
        */   
        this._http.joinRoom(this.room_token).subscribe((data: any)=>{
            //console.log(data);
            
        }
    )}

    removeUser(user_id: number){
        let u: any;
        for (u of this.room.users) {
            if(u.id==user_id){
                var index = this.room.users.indexOf(u);
                if (index > -1) {
                    this.room.users.splice(index, 1);
                }
            }
          }
    }

    addUser(user: any){
        let u: any;
        for (u of this.room.users) {
            if(u.id==user.id){
                return true;
            }
        }
        this.room.users.push(user);

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
        Отправка сообщения в чате
    */
    submit(): void{
        let obj = {"message": this.text_message, "room_token": this.room_token}
        this._http.saveMessage(obj,this.csrf_token).subscribe((data: any) => {
            //console.log(data);
            //if(data.is_true){
            //    this.getQuestion();
            //}
            this.text_message = '';
        });
    }

    /*
        change question
    */
    getQuestion(){
        this._http.getQuestion(this.room_token).subscribe(
            (data: any) => {
                this.room.question_text_ru = data.text_ru;
                this.room.question_text_en = data.text_en;
                this.room.question_lang = data.lang;
                this.room.current_question_number = data.current_question;
                this.is_first_question = false;
                this.show_next = true;
                this.inputBox.nativeElement.focus();
                
            }   
        );
    }

    /*
        get next question
    */
    nextQuestion(){
        this._http.nextQuestion(this.room_token).subscribe(
            (data: any) => {
                console.log(data);
                this.show_next = false;
                this.text_message = '';
            }   
        );
    }

    
    /*
        меняем вопрос
    */
    endQuiz(){
        this.room.is_done = true;
        this._http.getRoomWinner(this.room_token).subscribe((data: any) => {
            this.winner = data.user;
        });
    }

    /* отслеживаем клаву */
    keyPressHandler(code: number) {
        // Enter
        //console.log(code);
        if (code === 63 && this.show_next === true){
            this.nextQuestion();
        }
        if (code === 13){
            this.submit();
        }
    } 

    /*
        Выделение пользователя
    */
    selectUser(user_id: number){
       
        let u: any;
        for (u of this.room.users) {
            var index = this.room.users.indexOf(u);
            if(u.id==user_id){
                this.room.users[index]['isSelected'] = true;
            } else {
                this.room.users[index]['isSelected'] = false;
            }
        }
        console.log(this.room.users);
    }

    getUserStyle(user: any){
        const style = 'background: red';
        return style;
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


@Component({
    selector: 'quiz-app',
    templateUrl: 'room.html'
    
})
export class DefineRoomComponent { 

    token: string;

    constructor(private router:Router){
        
    }
    ngOnInit() {
        this.token = localStorage.getItem('current_token');
        this.router.navigateByUrl('/room/'+this.token);
    }
}