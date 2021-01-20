import sqlite3
from config import *

CONN = sqlite3.connect(DB_FILE, check_same_thread=False)  # not thread safe!
C = CONN.cursor()

person_cols = ['person_id', 'name']
category_level1_cols = ['category_id', 'category_name']
category_level2_cols = ['category_id', 'category_name', 'parent_id']
expense_cols = ['record_id', 'date', 'category_level1_id',
                'category_level2_id', 'person_id', 'amount', 'note']


def to_dict(query_result, columns):
    return [dict(zip(columns, qr)) for qr in query_result]


# persons table
def get_person(person_id: int) -> list[tuple[int, str]]:
    if person_id is None:
        C.execute('SELECT person_id, name FROM persons WHERE deleted=0')
    else:
        C.execute(
            'SELECT person_id, name FROM persons WHERE person_id=? AND deleted=0', (person_id,))
    return to_dict(C.fetchall(), person_cols)


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


# categories level1 table
def get_category_level1(category_id: int) -> list[tuple[int, str]]:
    if category_id is None:
        C.execute(
            'SELECT category_id, category_name FROM categories_level1 WHERE deleted=0')
    else:
        C.execute(
            'SELECT category_id, category_name FROM categories_level1 WHERE category_id=? AND deleted=0', (category_id,))
    return to_dict(C.fetchall(), category_level1_cols)


def modify_category_level1(category_id: int, category_name: str):
    C.execute('UPDATE categories_level1 SET category_name=:name WHERE category_id=:id AND deleted=0',
              dict(name=category_name, id=category_id))
    CONN.commit()


def delete_category_level1(category_id: int):
    C.execute(
        'UPDATE categories_level1 SET deleted=1 WHERE category_id=?', (category_id,))
    CONN.commit()


def new_category_level1(category_name: str):
    C.execute(
        'INSERT INTO categories_level1 (category_name, deleted) VALUES (?, 0)', (category_name,))
    CONN.commit()


# categories level2 table
def get_category_level2(category_id: int) -> list[tuple[int, str, int]]:
    if category_id is None:
        C.execute(
            'SELECT category_id, category_name, parent_id FROM categories_level2 WHERE deleted=0')
    else:
        C.execute(
            'SELECT category_id, category_name, parent_id FROM categories_level2 WHERE category_id=? AND deleted=0', (category_id,))
    return to_dict(C.fetchall(), category_level2_cols)


def modify_category_level2(category_id: int, category_name: str, parent_id: int):
    C.execute('UPDATE categories_level2 SET category_name=:name, parent_id=:pid WHERE category_id=:id AND deleted=0',
              dict(name=category_name, pid=parent_id, id=category_id))
    CONN.commit()


def delete_category_level2(category_id: int):
    C.execute(
        'UPDATE categories_level2 SET deleted=1 WHERE category_id=?', (category_id,))
    CONN.commit()


def new_category_level2(category_name: str, parent_id: int):
    C.execute(
        'INSERT INTO categories_level2 (category_name, parent_id, deleted) VALUES (?,?,0)', (category_name, parent_id))
    CONN.commit()


# get all categories
def get_all_categories() -> dict[tuple[int, str], list[tuple[int, str]]]:
    C.execute('''
        SELECT c1.category_id, c1.category_name, c2.category_id, c2.category_name
        FROM categories_level2 AS c2
        LEFT JOIN categories_level1 AS c1
        ON c2.parent_id=c1.category_id
        WHERE c1.deleted=0 and c2.deleted=0
    ''')
    query_result = C.fetchall()
    level1_names, children = {}, {}
    for level1_id, level1_name, level2_id, level2_name in query_result:
        if level1_id not in level1_names:
            level1_names[level1_id] = level1_name
        if level1_id in children:
            children[level1_id].append(
                {'level2_id': level2_id, 'level2_name': level2_name})
        else:
            children[level1_id] = [
                {'level2_id': level2_id, 'level2_name': level2_name}]
    categories = []
    for level1_id in level1_names:
        categories.append({
            "level1_id": level1_id,
            "level1_name": level1_names[level1_id],
            "level2_children": children[level1_id]
        })
    return categories


# expense table
def get_expense(record_id: int) -> list[tuple[int, str, int, int, int, float, str]]:
    if record_id is None:
        C.execute('SELECT record_id, date, category_level1_id, category_level2_id, person_id, amount, note FROM expenses WHERE deleted=0')
    else:
        C.execute(
            'SELECT record_id, date, category_level1_id, category_level2_id, person_id, amount, note FROM expenses WHERE record_id=? AND deleted=0', (record_id,))
    return to_dict(C.fetchall(), expense_cols)


def modify_expense(
    record_id: int,
    date: str,
    category_level1_id: int,
    category_level2_id: int,
    person_id: int,
    amount: float,
    note: str
):
    C.execute('''
        UPDATE expenses 
        SET date=?, category_level1_id=?, category_level2_id=?, person_id=?, amount=?, note=?
        WHERE record_id=? AND deleted=0
    ''', (date, category_level1_id, category_level2_id, person_id, amount, note, record_id))
    CONN.commit()


def delete_expense(record_id: int):
    C.execute(
        'UPDATE expenses SET deleted=1 WHERE record_id=?', (record_id,))
    CONN.commit()


def new_expense(
    date: str,
    category_level1_id: int,
    category_level2_id: int,
    person_id: int,
    amount: float,
    note: str
):
    C.execute('''
        INSERT INTO expenses 
        (date, category_level1_id, category_level2_id, person_id, amount, note, deleted)
        VALUES (?,?,?,?,?,?,0)
    ''', (date, category_level1_id, category_level2_id, person_id, amount, note)
    )
    CONN.commit()
