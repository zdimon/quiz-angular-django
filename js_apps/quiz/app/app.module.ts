import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {FormsModule , ReactiveFormsModule} from '@angular/forms';
import {AppComponent} from './app.component';
import { SocketService } from './utils';
import { QuizeService } from './http.service';
import { HttpClientModule } from '@angular/common/http';
import { ArraySortPipe } from './pipes'
import {QuestionsComponent} from './questions';
import {FilterComponent} from './questions';
import {RoomComponent, DefineRoomComponent, RoomHttpService} from './room';
import { RouterModule, Routes } from '@angular/router';
import {HashLocationStrategy, Location, LocationStrategy} from '@angular/common';
import * as $ from "jquery";
import { FacadeService } from './facade.service';
import { i18nService } from './i18n.service';
import { EditQuestionFormComponent, QuestionsHttpService } from './questions';
import {BaseHttp, WindowRefService} from './utils';
import { MainHttpService, CreateRoomFormComponent, MainComponent } from './main';


const room_token : any = $("quiz-app").attr('data-room-token');
//console.log(room_token)
const appRoutes: Routes = [
  
    { path: 'room/:token',      component: RoomComponent},
    { path: 'room',      component: DefineRoomComponent},
    { path: 'admin',      component: QuestionsComponent},
    { path: 'index',      component: MainComponent},
    { path: '',
      redirectTo: '/index',
      pathMatch: 'full'
    }
    /*
    { path: '',
      redirectTo: '/room/'+room_token,
      pathMatch: 'full'
    }
    */
  ];


@NgModule({
    imports:[
        BrowserModule, 
        FormsModule, 
        ReactiveFormsModule,
        HttpClientModule,
        RouterModule.forRoot(
            appRoutes
            //{ enableTracing: true } // <-- debugging purposes only
          )
    ],
    declarations: [
      AppComponent, 
      ArraySortPipe, 
      QuestionsComponent, 
      RoomComponent, 
      MainComponent, 
      FilterComponent,
      DefineRoomComponent,
      CreateRoomFormComponent,
      EditQuestionFormComponent
    ],
    bootstrap: [AppComponent],
    providers: [ 
        SocketService, 
        QuizeService, 
        WindowRefService,
        MainHttpService,
        FacadeService,
        i18nService,
        RoomHttpService,
        QuestionsHttpService,
        BaseHttp,
        {provide: LocationStrategy, useClass: HashLocationStrategy}
    ] 
})
export class AppModule{}
