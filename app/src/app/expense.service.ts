import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Expense } from './interface';


@Injectable({
  providedIn: 'root'
})
export class ExpenseService {
  private expensesUrl = 'http://localhost:5000/api/expense/';

  getExpenses(): Observable<Expense[]> {
    return this.http.get<Expense[]>(this.expensesUrl);
  }

  constructor(private http: HttpClient) { }
}
