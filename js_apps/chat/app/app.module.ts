import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {FormsModule} from '@angular/forms';
import {AppComponent} from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { ChatService } from './http.service';
import { SocketService } from './socket.service';
import { WindowRefService } from './window.service'
 
@NgModule({
    imports:[BrowserModule, FormsModule, HttpClientModule],
    declarations: [AppComponent],
    bootstrap: [AppComponent],
    providers: [ChatService, SocketService, WindowRefService] 
})
export class AppModule{}
