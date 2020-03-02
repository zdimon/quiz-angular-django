import { BaseHttp } from '../utils';
import { Injectable } from '@angular/core'; 
 
@Injectable()
export class MainHttpService extends BaseHttp{  

    public saveRoom(): any {
        var url = '/quiz/api/test';
        return this.makeRequest('get',url);
    }

}