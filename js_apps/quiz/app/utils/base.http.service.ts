import { Injectable } from '@angular/core'; 
//import { WindowRefService } from './utils';
import { WindowRefService } from './window.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Injectable()
export class BaseHttp { 

    private headers: any;
    public language: string;
    private _window: Window;
    

    constructor (protected http: HttpClient, windowRef: WindowRefService) {

        this._window = windowRef.nativeWindow;
        this.language = this._window['current_language'];
        this.headers = new HttpHeaders()
        .set('Content-Type', 'application/json')
        .set("Authorization", 'Token ' + this._window['current_user_token']);   

        
        
    }

    public makeRequest(method: string, url: string, data?: any): any { 

        if (method=='get'){
            return this.http
            .get('/'+this.language+url, { headers: this.headers }) 
        }

        if (method=='post'){
            return this.http
            .post('/'+this.language+url, data, { headers: this.headers })            
        }

        
        
    }    

}
