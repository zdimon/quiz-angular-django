import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FacadeService } from '../facade.service';

//https://translate.yandex.net/api/v1.5/tr.json/translate?lang=ru-en&key=trnsl.1.1.20140521T130035Z.1014ae2799c685e3.97b1345108ab3a8520d96f730016a9dac947049b&format=html&text=Фильтр для категорий
@Component({
    selector: 'edit-question-form',
    templateUrl: 'edit.question.form.html'
    
})
export class EditQuestionFormComponent { 

    i18n: any = {};
    private _http: any;
    private language: string;
    themes: any;
    @Input() obj: any = []; 
   
    constructor(private facade: FacadeService) {
       this._http = this.facade.httpService;
       this.language = this.facade.language;
    }

    @Output() submitEvent = new EventEmitter<any>();
        
    
    ngOnInit() {
        this.i18n = this.facade.i18nService.getI18n();
        this._http.getThemes().subscribe((data: any)=>{
            this.themes = data;
            this.themes.map((item: any) => {
                if(this.language=='ru'){
                    return item.name = item.name_ru
                }
                if(this.language=='en'){
                    return item.name = item.name_en
                }
            });
            //console.log(this.themes);
        });
    }
    
    setThemeStr(id: number){
        
        for (var i in this.themes){
            
            if (this.themes[i].id == id){
                
                if(this.language=='ru'){
                    return this.themes[i].name_ru;
                }
                if(this.language=='en'){
                    return this.themes[i].name_en;
                }
            }
        }        
    }

    submitForm(){
        //this.obj.theme = this.setThemeStr(this.obj.theme_id);
        this.submitEvent.emit(this.obj);
    }
      

    translate(direct: string, source: string) {
        
        
                if(direct=='en-ru') {
                    //console.log(this.pager.results[i].question_en); 

                    if(source == 'question') {
                        this.facade.httpService.translate(direct,this.obj.question_en,(data: any)=>{
                            this.obj.question_ru = data.text[0]
                        });   
                    }
                    if(source == 'answers') {
                        this.facade.httpService.translate(direct,this.obj.answers_en,(data: any)=>{
                            this.obj.answers_ru = data.text[0]
                        });   
                    }

                }
                if(direct=='ru-en') {
                    
                    if(source == 'question') {
                        this.facade.httpService.translate(direct,this.obj.question_ru,(data: any)=>{
                            this.obj.question_en = data.text[0]
                        });   
                    }

                    if(source == 'answers') {
                        this.facade.httpService.translate(direct,this.obj.answers_ru,(data: any)=>{
                            this.obj.answers_en = data.text[0]
                        });   
                    }


                }

             

        

    }    

}