import { Component, Input, Output, ElementRef, ViewChild} from '@angular/core';
import {Router} from '@angular/router';
import { FacadeService } from './facade.service';

@Component({
    selector: 'quiz-app',
    templateUrl: 'templates/base.html'
    
})
export class AppComponent { 

    i18n: any = {};
    lang: string;
    
    constructor (
        private router: Router,
        private facade: FacadeService
    ) {
        this.lang = this.facade.language;
    }    
   
    ngOnInit() {
        this.i18n = this.facade.i18nService.getI18n();
    }

}