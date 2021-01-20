from flask import Flask, request, jsonify
from db_func import *
app = Flask(__name__)


@app.route('/api/person/', methods=['GET', 'POST'])
@app.route('/api/person/<int:person_id>', methods=['GET', 'PUT', 'DELETE'])
def person(person_id: int = None):
    if request.method == 'GET':
        return jsonify(get_person(person_id))
    elif request.method == 'POST':
        name = request.json['name']
        new_person(name)
        return 'Success'
    elif request.method == 'PUT':
        name = request.json['name']
        modify_person(person_id, name)
        return 'Success'
    elif request.method == 'DELETE':
        delete_person(person_id)
        return 'Success'


@app.route('/api/category1/', methods=['GET', 'POST'])
@app.route('/api/category1/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category1(category_id: int = None):
    if request.method == 'GET':
        return jsonify(get_category_level1(category_id))
    elif request.method == 'POST':
        category_name = request.json['category_name']
        new_category_level1(category_name)
        return 'Success'
    elif request.method == 'PUT':
        category_name = request.json['category_name']
        modify_category_level1(category_id, category_name)
        return 'Success'
    elif request.method == 'DELETE':
        delete_category_level1(category_id)
        return 'Success'


@app.route('/api/category2/', methods=['GET', 'POST'])
@app.route('/api/category2/<int:category_id>', methods=['GET', 'PUT', 'DELETE'])
def category2(category_id: int = None):
    if request.method == 'GET':
        return jsonify(get_category_level2(category_id))
    elif request.method == 'POST':
        category_name, parent_id = request.json['category_name'], request.json['parent_id']
        new_category_level2(category_name, parent_id)
        return 'Success'
    elif request.method == 'PUT':
        category_name, parent_id = request.json['category_name'], request.json['parent_id']
        modify_category_level2(category_id, category_name, parent_id)
        return 'Success'
    elif request.method == 'DELETE':
        delete_category_level2(category_id)
        return 'Success'


@app.route('/api/all-categories/', methods=['GET'])
def categories():
    return jsonify(get_all_categories())


@app.route('/api/expense/', methods=['GET', 'POST'])
@app.route('/api/expense/<int:record_id>', methods=['GET', 'PUT', 'DELETE'])
def expense(record_id: int = None):
    if request.method == 'GET':
        return jsonify(get_expense(record_id))
    elif request.method == 'POST':
        date, category_level1_id, category_level2_id, person_id, amount, note = map(
            lambda k: request.json[k],
            ['date', 'category_level1_id', 'category_level2_id',
                'person_id', 'amount', 'note']
        )
        new_expense(date, category_level1_id,
                    category_level2_id, person_id, amount, note)
        return 'Success'
    elif request.method == 'PUT':
        date, category_level1_id, category_level2_id, person_id, amount, note = map(
            lambda k: request.json[k],
            ['date', 'category_level1_id', 'category_level2_id',
                'person_id', 'amount', 'note']
        )
        modify_expense(record_id, date, category_level1_id,
                       category_level2_id, person_id, amount, note)
        return 'Success'
    elif request.method == 'DELETE':
        delete_expense(record_id)
        return 'Success'
