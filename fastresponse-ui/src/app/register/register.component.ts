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
  userId: string;
  
  constructor(private regService: RegisterService) { }

  ngOnInit() {
  }

  onSubmit(){
    this.regService.add(this.user).subscribe(user => {
      this.user = new UserInput();
      console.log(user.id + 'was found');
      this.userId = user.id;
      
    });
    console.log(this.user.name, this.user.address);
  }

}
