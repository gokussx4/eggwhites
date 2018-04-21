import { Injectable } from '@angular/core';
import{UserInput} from './register/userInput';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';


@Injectable()
export class RegisterService {

  constructor(private http: HttpClient) { }

  baseUrl = 'http://localhost:8080';
  add(user: UserInput): Observable<UserInput> {
    return this.http.post<UserInput>('/api/v0/user', user);
  }

}
