import { BaseHttp } from '../utils';
import { Injectable } from '@angular/core'; 
 
@Injectable()
export class QuestionsHttpService extends BaseHttp{  

    public testAction(): any {
        var url = '/quiz/api/test';
        return this.makeRequest('get',url);
    }

}