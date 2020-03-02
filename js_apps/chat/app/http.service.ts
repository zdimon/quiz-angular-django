import { Injectable } from '@angular/core'; 
import { HttpClient, HttpHeaders } from '@angular/common/http';

import {Observable} from 'rxjs/Rx';
import 'rxjs/add/operator/map'; 


 
 @Injectable()
 export class ChatService {  

 
    headers: any;
    language: string;


    constructor (private http: HttpClient) {
        this.headers = new HttpHeaders()
        .set('Content-Type', 'application/json');
        
    }

    public init(language: string){
       
        this.language = language;     
    }    
   
   

    public saveMessage(obj: any): any { 
        
        return this.http
        .post('/'+this.language+'/chat/submit',obj, { headers: this.headers })
        
        
    }  

    public getI18n(language: string): any { 
        return this.http
        .get('/'+language+'/quiz/api/i18n', { headers: this.headers }) 
        
    }    
    
    public getMessages(): any { 
        return this.http
        .get('/'+this.language+'/chat/get_messages', { headers: this.headers }) 
        
    }   
    
    public nextQuestion(): any { 
        return this.http
        .get('/'+this.language+'/chat/next_question', { headers: this.headers })    
    }  
    

    
 } 
