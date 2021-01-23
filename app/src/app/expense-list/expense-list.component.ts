import { Expense } from './../interface';
import { ExpenseService } from './../expense.service';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-expense-list',
  templateUrl: './expense-list.component.html',
  styleUrls: ['./expense-list.component.css']
})
export class ExpenseListComponent implements OnInit {
  expenses: Observable<Expense[]> = this.expenseService.getExpenses();

  constructor(private expenseService: ExpenseService) { }

  ngOnInit(): void {
  }

}
