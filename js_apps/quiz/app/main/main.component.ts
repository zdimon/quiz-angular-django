import { Component, Input, Output, ElementRef, ViewChild} from '@angular/core';
import { SocketService } from '../utils';  
import { QuizeService } from '../http.service'; 
import { ArraySortPipe } from '../pipes'
import * as $ from "jquery"; 


//console.log(QuizeService);

@Component({
    selector: 'admin',
    templateUrl: 'main.html'
    
})
export class MainComponent { 

    i18n: any = {};
    active_rooms: any = []; 
   
    constructor(private _http: QuizeService) {
       
    }
    
    ngOnInit() {
        // get I18n messages
        this._http.getI18n().subscribe((data: any) => {
            this.i18n = data;
        });
        this._http.getActiveRooms().subscribe((data: any) => {
            this.active_rooms = data.rooms;
            //console.log(this.active_rooms);
        });

    }
    
      

}