from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe_model
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
import pprint

db = 'RecipeDB_'


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.recipe = []

    @classmethod
    def create_user(cls, data):
        sql = "INSERT INTO users (first_name,last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL(db).query_db(sql, data)


    @classmethod
    def get_user_by_email(cls, data):
        sql = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(sql, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one_user(cls, user_id):
        sql = 'SELECT * FROM users WHERE id = %(id)s'
        results = connectToMySQL(db).query_db(sql, {'id': user_id})
        return cls(results[0])


    @classmethod
    def get_all_users(cls):
        sql = 'SELECT * FROM users'
        results = connectToMySQL(db).query_db(sql)
        pprint.pprint(results, sort_dicts=False)
        users = []
        for user in results:
            return users.append(cls(user))
        return users

    @classmethod
    def get_one_user_with_recipes(cls, user_id):
        sql = 'SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.user_id WHERE users.id = %(id)s'
        data = {
            'id': user_id
        }
        results = connectToMySQL(db).query_db(sql, data)
        pprint.pprint(results, sort_dicts=False)
        users = cls(results[0])
        for u in results:
            recipe_data = {
                'id': u['recipes.id'],
                'name': u['name'],
                'description': u['description'],
                'instructions': u['instructions'],
                'under': u['under'],
                'created_at' : u['recipes.created_at'],
                'updated_at' : u['recipes.updated_at'],
                'user_id': u['user_id']
            }
            users.recipe.append(recipe_model.Recipe(recipe_data))
        return users



    @staticmethod
    def validate_user1(user):
        is_valid = True
        sql = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(sql, user)

        if len(results) >= 1:
            flash("Email already taken.","register")
            is_valid=False

        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email!!!","register")
            is_valid=False

        if len(user['first_name']) < 2:
            flash("First name must be at least 3 characters long","register")
            is_valid= False

        if len(user['last_name']) < 2:
            flash("Last name must be at least 3 characters", "register")
            is_valid= False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid= False

        if user['password'] != user['confirm_password']:
            flash("Passwords do not match!", "register")

        return is_valid


    @staticmethod
    def validate_user2(user):
        is_valid = True
        sql = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(db).query_db(sql, user)

        return is_valid