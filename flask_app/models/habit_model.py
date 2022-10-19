from pprint import pprint
from flask_app import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User

DATABASE = 'habits_schema'


class Habit:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.user_id = data['user_id']
        self.creator = data['user']

    def __repr__(self):
        return f'<Habit: {self.setup}>'


    @staticmethod
    def validate_habit(form):
        is_valid = True
        if len(form['title']) < 2:
            flash('title must be at least two characters.', 'title')
            is_valid = False
        if len(form['description']) < 10:
            flash('description must be at least ten characters.', 'description')
            is_valid = False
        if not int(form['price']) >0: 
            flash('Price must be greater than 0', 'price' )
            is_valid = False
        return is_valid

    # create a habit
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO habits (title, description, price, user_id) VALUES( %(title)s, %(description)s, %(price)s, %(user_id)s);'
        habit_id = connectToMySQL(DATABASE).query_db(query, data)
        return habit_id

    # find all habits (no data needed)
    @classmethod
    def find_all(cls):
        query = 'SELECT * from habits;'
        results = connectToMySQL(DATABASE).query_db(query)
        pprint(results)
        habits = []
        for result in results:
            user_data = {
                'id': result['user_id']
            }
            user = User.find_by_id(user_data)
            habit_data = {
                'id': result['id'],
                'title': result['title'],
                'description': result['description'],
                'price': result['price'],
                'user_id': result['user_id'],
                'user': user,
            }
            habit = Habit(habit_data)
            habits.append(habit)
        return habits

    # find one habit by id
    @classmethod
    def find_by_id(cls, data):
        query = 'SELECT * from habits WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        habit = Habit(results[0])
        return habit

    # find one habit by id with creator
    @classmethod
    def find_by_id_with_creator(cls, data):
        query = 'SELECT * from habits WHERE id = %(id)s;'
        results = connectToMySQL(DATABASE).query_db(query, data)
        pprint(results)
        user_data = {
            'id': results[0]['user_id']
        }
        user = User.find_by_id(user_data)
        habit_data = {
            'id': results[0]['id'],
            'title': results[0]['title'],
            'description': results[0]['description'],
            'price': results[0]['price'],
            'user_id': results[0]['user_id'],
            'user': user,
        }
        habit = Habit(habit_data)
        return habit

    # update one habit by id
    @classmethod
    def find_by_id_and_update(cls, data):
        query = 'UPDATE habits SET title = %(title)s, description = %(description)s, price = %(price)s WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True

    # delete one habit by id
    @classmethod
    def find_by_id_and_delete(cls, data):
        query = 'DELETE FROM habits WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return True
