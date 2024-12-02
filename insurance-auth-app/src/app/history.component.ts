import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-history',
  standalone: true,
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css'],
  imports: [CommonModule, NgIf, NgFor]
})
export class HistoryComponent implements OnInit {
  history: any[] = [];

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.getHistory();
  }

  getHistory() {
    const token = localStorage.getItem('token');
    if (!token) {
      console.log('No token found');
      this.history = [];
      return;
    }

    this.http.get<any>('http://127.0.0.1:5000/api/history', {
      headers: {
        'x-access-token': token
      }
    }).subscribe(
      (response) => {
        console.log('History data received:', response);
        this.history = response.history || [];
        if (this.history.length === 0) {
          console.log('No history items found');
        }
      },
      (error) => {
        console.error('Error fetching history:', error);
        this.history = [];
      }
    );
  }
}
