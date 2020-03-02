import { Injectable, Injector } from '@angular/core'; 
import { i18nService } from './i18n.service';
import { QuizeService } from './http.service';
import { WindowRefService } from './utils';

//export { EditQuestionFormComponent } from './forms/edit.question.form.component';
 
 @Injectable()
 export class FacadeService {  

    private  _i18n: i18nService;
    private _http: QuizeService;
    private _window: Window;

    constructor(private injector: Injector, windowRef: WindowRefService){
        this._window = windowRef.nativeWindow;
    }

    public get i18nService(){
        this._i18n = this.injector.get(i18nService);
        return this._i18n;
    }

    public get httpService(){
        this._http = this.injector.get(QuizeService);
        return this._http;
    }

    public get language(){
       return this._window['current_language'];
    }


 } 
