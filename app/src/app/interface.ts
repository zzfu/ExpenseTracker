export interface Expense {
    record_id: number;
    date: string;
    category_level1_id: number;
    category_level2_id: number;
    person_id: number;
    amount: number;
    note: string;
}