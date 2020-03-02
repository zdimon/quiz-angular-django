import { Injectable } from '@angular/core'; 
import { WindowRefService } from './utils';


 
 @Injectable()
 export class i18nService {  
    private _window: Window;
 
   
    constructor (windowRef: WindowRefService) {
        this._window = windowRef.nativeWindow;
    }

    getI18n(){
        return this._window['i18n'];
    }



 } 
