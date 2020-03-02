import { Injectable } from '@angular/core'; 
//import {Http, Response, Headers, RequestOptions} from '@angular/http';
import { HttpClient, HttpHeaders } from '@angular/common/http'; 
import {Observable} from 'rxjs/Rx';
import 'rxjs/add/operator/map'; 
import { WindowRefService } from './utils';
//import { WindowRefService } from './window.service';



 
 @Injectable()
 export class QuizeService {  

 
    headers: any;
    //language: string = localStorage.getItem('current_language');
    language: string = $("quiz-app").attr('data-language');
    user_token: string = $("quiz-app").attr('data-user-token');
   //user_token: string = localStorage.getItem('user_token');
    

    constructor (private http: HttpClient) {
        this.headers = new HttpHeaders()
        .set('Content-Type', 'application/json')
        .set("Authorization", 'Token ' + this.user_token);   
        
    }

    /*
    public init_token(token: string, language: string){
        this.headers = new HttpHeaders().set("Authorization", 'Token ' + token);   
        this.language = language;     
    }
    */
     
    public getRoomInfo(token: string): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/room/'+token+'/info', { headers: this.headers }) 
        
    }

    public joinRoom(token: string): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/room/'+token+'/join', { headers: this.headers }) 
        
    }

    public getQuestion(token: string): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/room/'+token+'/question', { headers: this.headers }) 
        
    }    

    public getRoomUsers(token: string): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/room/'+token+'/users', { headers: this.headers }) 
        
    }

    public getUserInfo(token: string, user_id: number): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/room/'+token+'/user/'+user_id+'/detail', { headers: this.headers }) 
        
    }

    public getRoomWinner(token: string): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/room/'+token+'/winner', { headers: this.headers }) 
        
    }

    public saveMessage(obj: any, token: string): any { 
        
        return this.http
        .post('/'+this.language+'/quiz/api/room/submit',obj, { headers: this.headers })
        
        
    }  

    public getI18n(): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/i18n', { headers: this.headers }) 
        
    }    

   
    
    public changeLang(lang: string): any { 
        return this.http
        .get('/'+lang+'/quiz/api/i18n', { headers: this.headers }) 
        
    }   
   

    public nextQuestion(room_token: string): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/room/'+room_token+'/next_question', { headers: this.headers }) 
        
    }    

    public getActiveRooms(): any { 
        return this.http
        .get('/'+this.language+'/quiz/api/get_active_rooms', { headers: this.headers }) 
        
    } 

    public getQuestions(limit: number,offset: number, filter: any): any { 
        
        var uri = '/'+this.language+'/quiz/api/questions/?limit='+limit+'&offset='+offset;
        for (let i in filter) {
            
            uri = uri + '&' + i + '=' + filter[i]
        }
        
        return this.http
        .get(uri, { headers: this.headers }) 
        
    } 

    public getThemes(): any { 

        return this.http
        .get('/'+this.language+'/quiz/api/theme', { headers: this.headers }) 
        
    } 

    public saveQuestion(obj: any): any { 
        
        return this.http
        .post('/'+this.language+'/quiz/api/admin/save/question',obj, { headers: this.headers })
        
        
    } 

    public deleteQuestion(obj: any): any { 
        
        return this.http
        .post('/'+this.language+'/quiz/api/admin/delete/question',obj, { headers: this.headers })
        
        
    } 

    

    public publishQuestion(id: number): any { 
        
        return this.http
        .get('/'+this.language+'/quiz/api/admin/publish/'+id+'/question', { headers: this.headers })
        
        
    } 
    
    public unpublishQuestion(id: number): any { 
        
        return this.http
        .get('/'+this.language+'/quiz/api/admin/unpublish/'+id+'/question', { headers: this.headers })
        
        
    } 

    /*
        starting-account-ub2dgvf7bqua.
    */

    public translate(direct: string, txt: string, clb: (data: any)=>any): any { 

        /*
        let uri = `https://translate.yandex.net/api/v1.5/tr.json/translate?lang=ru-en&key=trnsl.1.1.20140521T130035Z.1014ae2799c685e3.97b1345108ab3a8520d96f730016a9dac947049b&format=html&text=${txt}`
        console.log(uri)
        return this.http
        .get(uri)

        */
       var apiUrl = "https://translate.yandex.net/api/v1.5/tr.json/translate";
       var apiData = {
            error: 'onTranslationError',
            success: 'onTranslationComplete',
            lang: 'en',
            key: 'trnsl.1.1.20140521T130035Z.1014ae2799c685e3.97b1345108ab3a8520d96f730016a9dac947049b',
            format: 'html',
            text: txt
        };

        $.ajax({
            url: apiUrl,
            data: apiData,
            dataType: 'jsonp',
            success: function(response) {
                if (response.code == 200) {
                    //console.log(response.text[0].replace(/<br>/g, '\n').replace(/&lt;/g, '<').replace(/&gt;/g, '>'));
                    console.log(response);
                    clb(response);
                    
                } else {
                    console.log(response);
                }
            },
            error: function(response) {
                console.log(response);
            }
        });
        
        
    } 


 } 
