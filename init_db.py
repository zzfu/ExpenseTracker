import sqlite3
from config import *


def init_persons_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    with open(PERSON_FILE, 'r') as f:
        persons = [(line.strip(), ) for line in f.readlines()]
    c.executemany('''
        INSERT INTO persons (name, deleted) VALUES (?,0)
    ''', persons)
    conn.commit()
    conn.close()


def init_categories_table():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    with open(CATEGORY_FILE, 'r') as f:
        lines = f.readlines()
    level1_categories = []
    level2_categories = []
    parent_name = ''
    for line in lines:
        line = line.strip()
        level, name = line.split(' ', maxsplit=1)
        level = len(level)
        if level == 1:
            parent_name = name
            level1_categories.append(name)
        elif level == 2:
            level2_categories.append((name, parent_name))
        else:
            raise NotImplementedError()
    for name in level1_categories:
        c.execute('''
            INSERT INTO categories_level1 (category_name, deleted) VALUES (?, 0)
        ''', (name,)
        )
    conn.commit()
    for name, parent_name in level2_categories:
        c.execute('''
            SELECT category_id FROM categories_level1 where category_name=?
        ''', (parent_name,)
        )
        parent_id = c.fetchone()[0]
        c.execute('''
            INSERT INTO categories_level2 (category_name, parent_id, deleted) VALUES (?, ?, 0)
        ''', (name, parent_id)
        )
        conn.commit()
    conn.close()


if __name__ == '__main__':
    init_persons_table()
    init_categories_table()
