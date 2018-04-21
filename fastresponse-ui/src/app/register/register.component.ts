import { Component, OnInit } from '@angular/core';
import {UserInput} from './userInput';
import { RegisterService } from '../register.service';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  
  user: UserInput = new UserInput();

  constructor(private regService: RegisterService) { }

  ngOnInit() {
  }

  onSubmit(){
    this.regService.add(this.user).subscribe(user => {
      this.user = user;
      console.log(user.id + 'was found');
    });
    console.log(this.user.name, this.user.address);
  }

}
