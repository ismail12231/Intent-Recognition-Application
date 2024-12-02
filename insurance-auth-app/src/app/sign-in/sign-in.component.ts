import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common'; 

@Component({
  selector: 'app-sign-in',
  standalone: true,
  imports: [FormsModule, CommonModule], 
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.css']
})
export class SignInComponent {
  credentials = {
    username: '',
    password: ''
  };

  isLoggedIn = false;

  constructor(
    private http: HttpClient,
    private router: Router,
    private cdr: ChangeDetectorRef
  ) {}

  onSubmit() {
    this.http.post('http://127.0.0.1:5000/login', this.credentials)
      .subscribe({
        next: (response: any) => {
          alert('Login successful!');
          localStorage.setItem('token', response.token);
          this.isLoggedIn = true;
          this.cdr.detectChanges();
        },
        error: (error) => {
          alert('Login failed. Please check your credentials and try again.');
        }
      });
  }

  navigateTo(destination: string) {
    if (destination === 'request') {
      this.router.navigate(['/request']);
    } else if (destination === 'history') {
      this.router.navigate(['/history']);
    }
  }
}
