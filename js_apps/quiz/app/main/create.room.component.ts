import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FacadeService } from '../facade.service';
import { FormControl, FormGroup, FormArray, Validators, FormBuilder } from '@angular/forms'
import { MainHttpService } from './main.http.service'


@Component({
    selector: 'create-room-form',
    templateUrl: 'create.room.form.html'
    
})
export class CreateRoomFormComponent { 

    i18n: any = {};
    room: any = { name: '', themes: [], types: [] ,type: 'questionend'};
    themes: any = [];
    formModel: FormGroup;
    private language: string;

    constructor(private facade: FacadeService, private fb: FormBuilder, private _http: MainHttpService) {
       this.language = this.facade.language;
       this.formModel = this.fb.group({
           name: '',
           themes: this.fb.array([])
       });
    }

    handleSubmit(){
        console.log(this.formModel.value);
        //console.log(this.formModel.valid);
    }
    
    ngOnInit() {
        this.i18n = this.facade.i18nService.getI18n();
        this.room.types = [
            {type: 'questionend', name: this.i18n.questionend},
            {type: 'infinite', name: this.i18n.infinite},
            {type: 'custom', name: this.i18n.custom},
        ]
        
        this.facade.httpService.getThemes().subscribe((data: any) => {
            data = data.map((item: any) => {
                item.is_selected = false;
                item.name = item['name_'+this.language];
                return item;
            });
            this.room.themes = data;
            var themeFG = this.themes.map((item: any) => {
                let obj = {title: item['name_'+this.language], selected: true, value: item.id};
                return this.fb.group(obj);
                //console.log(item);
            });
            var themeFormArray = this.fb.array(themeFG);
            //console.log(themeFG);
            //console.log(themeFormArray);
            this.formModel.setControl('themes',themeFormArray);
            //console.log(themeFormArray);
            // form initialization



            //console.log(this.themes);
        });
    }
    
    submitForm(){
        console.log(this.room.themes);
        this._http.saveRoom().subscribe((data: any) => {
            console.log(data);
        });
    }

    themeChange(e: any){
        // find name of the theme
        for(let i of this.room.themes){
            if(i.id===parseInt(e.target.id)){
                var arr_name = this.room.name.split(', ').filter((val: any) => val);
                if(i.is_selected){
                    arr_name.push(i['name_'+this.language]);
                } else {
                    var index = arr_name.indexOf(i['name_'+this.language]);
                    if (index > -1) {
                        arr_name.splice(index, 1);
                      }
                }
                this.room.name = arr_name.join(', ')
            }
        }
    }

    get themecheckbox(){
        return this.formModel.get('themes');
    }

}