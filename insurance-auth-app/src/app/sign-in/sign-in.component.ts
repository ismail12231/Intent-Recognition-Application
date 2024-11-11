import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';  // Import FormsModule
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [FormsModule],  // Add FormsModule here
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent {
  credentials = {
    username: '',
    password: ''
  };

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit() {
    this.http.post('http://127.0.0.1:5000/login', this.credentials)
      .subscribe({
        next: (response: any) => {
          alert('Login successful!');
          localStorage.setItem('token', response.token);
          this.router.navigate(['/dashboard']);
        },
        error: (error) => {
          alert('Login failed. Please check your credentials and try again.');
        }
      });
  }
}
