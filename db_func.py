import sqlite3
from config import *


CONN = sqlite3.connect(DB_FILE)
C = CONN.cursor()


# persons table
def get_person(person_id: int) -> list[str]:
    if person_id is None:
        C.execute('SELECT name FROM persons WHERE deleted=0')
    else:
        C.execute(
            'SELECT name FROM persons WHERE person_id=? AND deleted=0', (person_id,))
    return [record[0] for record in C.fetchall()]


def modify_person(person_id: int, name: str):
    C.execute('UPDATE persons SET name=:name WHERE person_id=:id AND deleted=0',
              dict(name=name, id=person_id))
    CONN.commit()


def delete_person(person_id: int):
    C.execute('UPDATE persons SET deleted=1 WHERE person_id=?', (person_id,))
    CONN.commit()


def new_person(name: str):
    C.execute('INSERT INTO persons (name, deleted) VALUES (?, 0)', (name,))
    CONN.commit()


# categories table
def get_all_categories() -> dict[str, list[str]]:
    C.execute('''
        SELECT c1.category_name, c2.category_name
        FROM categories_level2 AS c2
        LEFT JOIN categories_level1 AS c1
        ON c2.parent_id == c1.category_id
    ''')
    categories = {}
    query_result = C.fetchall()
    for level1_name, level2_name in query_result:
        if level1_name in categories:
            categories[level1_name].append(level2_name)
        else:
            categories[level1_name] = [level2_name]
    return categories


def insert_expense_record(date, category_level1, category_level2, person, amount, note):
    C.execute('''
        SELECT category_id FROM categories_level1 WHERE category_name=?
    ''', (category_level1, ))
    level1_id = C.fetchone()[0]
    C.execute('''
        SELECT category_id FROM categories_level2 WHERE category_name=?
    ''', (category_level2, ))
    level2_id = C.fetchone()[0]
    C.execute('''
       SELECT person_id FROM persons WHERE name=?
    ''', (person, ))
    person_id = C.fetchone()[0]
    C.execute('''
        INSERT INTO expenses 
        (date, category_level1_id, category_level2_id, person_id, amount, note, deleted)
        VALUES (?,?,?,?,?,?,0)
    ''', (date, level1_id, level2_id, person_id, amount, note)
    )
    CONN.commit()
