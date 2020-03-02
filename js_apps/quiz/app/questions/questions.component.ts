import { Component, Input, Output, ElementRef, ViewChild} from '@angular/core';
import { SocketService } from '../utils';   
import { ArraySortPipe } from '../pipes'
import { FacadeService } from '../facade.service';
import * as $ from "jquery"; 
//console.log(QuizeService);

@Component({
    selector: 'admin',
    templateUrl: 'questions.html'
    
})
export class QuestionsComponent { 
   private _http: any;
   limit: number = 10;
   offset: number = 0;
   pager: any = {};
   i18n: any = {};
   edit_obj = {
    "id": "",
    "question_ru": "",
    "question_en": "",
    "answers_ru": "",
    "answers_en": "",
    "theme_id": 326,
    "lang": "",
    "level": 1
    };
   filter = {};
   language: string = $("quiz-app").attr('data-language');
   new_obj = {
       "question_ru": "",
       "question_en": "",
       "answers_ru": "",
       "answers_en": "",
       "level": 1,
       "lang": "",
       "theme_id": 326,
       "is_new": true
   };
   create_question = false;
   is_filtered = false;

   constructor( 
                private facade: FacadeService
                
              ) {           
        this._http = this.facade.httpService;
    }

   ngOnInit(){
    this.filter = JSON.parse(localStorage.getItem('current_filter'));
    if(this.filter) { this.is_filtered = true }
    if(!this.filter){this.filter = {}};
    this.i18n = this.facade.i18nService.getI18n();
    this.goPage(this.limit, this.offset, this.filter);
    
   }

   goPage(limit: number,offset: number, filter: any){
        this.offset = limit*offset;
        this.pager = this._http.getQuestions(limit,this.offset, this.filter).subscribe(
            (data: any) => {
                this.pager = data;
            }
        );        
   }

   editQuestion(id: number){
    
    
        for (var i in this.pager.results){
                this.pager.results[i].is_edit = false;  
        }
        for (var i in this.pager.results){
            if (this.pager.results[i].id == id){
                this.pager.results[i].is_edit = true;
                this.edit_obj = this.pager.results[i];
            }    
        }
        
   }

   submitForm(obj: any){
       

        this._http.saveQuestion(obj).subscribe((data: any) => {
            if (data.status==1){
                alert(data.message);
            }
            //console.log(data);
            if(data.is_new){ 
                this.goPage(this.limit, this.offset, this.filter);
                this.new_obj = {
                    "question_ru": "",
                    "question_en": "",
                    "answers_ru": "",
                    "answers_en": "",
                    "level": 1,
                    "lang": "",
                    "theme_id": data.object.theme_id,
                    "is_new": true
                };
            } else {
                this.goPage(this.limit, this.offset, this.filter);
                /*
                for (var i in this.pager.results){
                    if (this.pager.results[i].id == data.object.id){
                        this.pager.results[i] = data.object;
                        this.pager.results[i].is_edit = false;
                    }    
                }
                */
            }
        });
           
    }   

       

    deleteQuestion(id: number) {

        //if(confirm("Are you sure?")) {
           
            var obj = { "id": id }
            this._http.deleteQuestion(obj).subscribe((data: any) => {
                if (data.status == 1) {
                    alert(data.message);
                } else { 
                    

                    this.goPage(this.pager.limit, this.pager.offset, this.filter);
                }
            });          
        //}
    }


    

    publishQuestion(id: number) {           
            this._http.publishQuestion(id).subscribe((data: any) => {
                if (data.status == 1) {
                    alert(data.message);
                } else { 
                    for (var i in this.pager.results){
                        if (this.pager.results[i].id == id){
                            this.pager.results[i].is_published = true;
                        }    
                    }
                }
            });          
    }    

    unpublishQuestion(id: number) {

        this._http.publishQuestion(id).subscribe((data: any) => {
            if (data.status == 1) {
                alert(data.message);
            } else { 
                for (var i in this.pager.results){
                    if (this.pager.results[i].id == id){
                        this.pager.results[i].is_published = false;
                    }    
                }
            }
        });          
    
    }    

    handleFilter($emit: any){
        this.is_filtered = true;
        this.filter[$emit.type] = $emit.id;
        var f: any = JSON.parse(localStorage.getItem('current_filter'));
        //console.log(f);
        if(!f){ f = {};}
        f[$emit.type] = $emit.id;
        localStorage.setItem('current_filter', JSON.stringify(f));
        //console.log($emit);
        // trigger page on 1
        this.offset = 1;
        this.goPage(this.limit, this.offset, this.filter);
    }

    clearFilter(){
        this.is_filtered = false;
        this.filter = {};
        localStorage.removeItem('current_filter');
        this.goPage(this.limit, this.offset, this.filter);
    }

    newQuestion() {
        this.create_question = true;
    }




}