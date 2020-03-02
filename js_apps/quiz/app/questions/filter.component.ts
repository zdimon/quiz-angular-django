import { Component, Input, Output, EventEmitter, ElementRef, ViewChild} from '@angular/core';
import { QuizeService } from '../http.service';
import * as $ from "jquery"; 

@Component({
    selector: 'filter',
    templateUrl: 'filter.html'
    
})
export class FilterComponent { 
    themes: any = [];
    filter: any = {};
    @Input() language: string;
    @Input() current_filter: any;

    @Output() filterOn = new EventEmitter<any>();


   constructor(private _http: QuizeService) { }
    

   ngOnInit(){
        this._http.getThemes().subscribe((data: any) => {
            this.themes = data;
            console.log(this.language);
        });       
   }

   submitFilter(id: number, type: string){
        this.filter[type] = id;
        this.filterOn.emit({"id":id, "type": type});
   }
}