import sqlite3
from config import *


def create_persons_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE persons (
            person_id INTEGER PRIMARY KEY,
            name TEXT, 
            deleted INTEGER, 
            UNIQUE(name, deleted)
        )
    ''')
    conn.commit()
    conn.close()


def create_categories_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE categories_level1 (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT UNIQUE,
            deleted INTEGER, 
            UNIQUE(category_name, deleted)
        )
    ''')
    c.execute('''
        CREATE TABLE categories_level2 (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT, 
            parent_id INTEGER, 
            deleted INTEGER, 
            UNIQUE(parent_id, category_name, deleted)
        )
    ''')
    conn.commit()
    conn.close()


def create_expenses_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE expenses (
            record_id INTEGER PRIMARY KEY,
            date DATE,
            category_level1_id INTEGER,
            category_level2_id INTEGER,
            person_id INTEGER,
            amount REAL,
            note TEXT, 
            deleted INTEGER
        )
    ''')
    conn.commit()
    conn.close


if __name__ == '__main__':
    create_persons_table()
    create_categories_table()
    create_expenses_table()
