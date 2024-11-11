import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-up',
  standalone: true,
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
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
    // Debugging output to ensure form data is correct
    console.log('Form Submitted:', this.user);

    // Check if all fields are filled
    if (!this.user.username || !this.user.email || !this.user.password) {
      alert('All fields are required. Please fill them out correctly.');
      return;
    }

    // Validate email format (simple regex)
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    if (!emailPattern.test(this.user.email)) {
      alert('Please enter a valid email address.');
      return;
    }

    // Send sign-up request
    this.http.post('http://127.0.0.1:5000/signup', this.user).subscribe({
      next: (response) => {
        console.log('User created successfully:', response);
        alert('User created successfully! Please Sign In.');
        // Redirect to the Sign In page after successful registration
        this.router.navigate(['/sign-in']);
      },
      error: (error) => {
        console.error('Error during Sign Up:', error);
        if (error.status === 409) {
          alert('User with this username or email already exists.');
        } else {
          alert('Sign Up failed. Please try again.');
        }
      }
    });
  }
}
