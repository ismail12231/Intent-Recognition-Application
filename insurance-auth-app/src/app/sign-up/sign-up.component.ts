import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
  standalone: true,
  imports: [FormsModule, CommonModule]
})
export class SignUpComponent {
  user = {
    username: '',
    email: '',
    password: ''
  };

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit() {
    this.http.post('http://127.0.0.1:5000/signup', this.user).subscribe({
      next: (response) => {
        alert('User created successfully! Please Sign In.');
        this.router.navigate(['/sign-in']);
      },
      error: (error) => {
        if (error.status === 409) {
          alert('User with this username or email already exists.');
        } else {
          alert('Sign Up failed. Please try again.');
        }
      }
    });
  }
}
