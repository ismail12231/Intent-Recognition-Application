import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-request-submission',
  standalone: true,
  templateUrl: './request-submission.component.html',
  styleUrls: ['./request-submission.component.css'],
  imports: [ReactiveFormsModule, CommonModule]  
})
export class RequestSubmissionComponent {
  requestForm: FormGroup;
  responseMessage: string = '';

  constructor(private fb: FormBuilder, private http: HttpClient) {
    this.requestForm = this.fb.group({
      requestText: ['', Validators.required]
    });
  }

  submitRequest() {
    const requestText = this.requestForm.value.requestText;

    if (!requestText) {
      this.responseMessage = 'Request text is required';
      return;
    }

    const token = localStorage.getItem('token');
    if (!token) {
      this.responseMessage = 'You must be logged in to submit a request.';
      return;
    }

    this.http.post<any>('http://127.0.0.1:5000/api/request', { request_text: requestText }, {
      headers: {
        'x-access-token': token
      }
    }).subscribe(
      (response) => {
        this.responseMessage = `Request submitted successfully. Intent classified as: ${response.intent}`;
      },
      (error) => {
        this.responseMessage = 'Failed to submit request. Please try again later.';
      }
    );
  }
}
