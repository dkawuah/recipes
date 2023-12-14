from flask_app.models import user_model
from flask_app.models import recipe_model
from flask_app.config.mysqlconnection import connectToMySQL
import pprint

db = 'RecipeDB_'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.under = data['under']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def create_recipe(cls, data):
        sql = 'INSERT INTO recipes (name, description, instructions, under, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under)s, %(user_id)s);'
        return connectToMySQL(db).query_db(sql, data)

    @classmethod
    def get_one_recipe(cls, user_id):
        sql = 'SELECT * FROM recipes WHERE id = %(id)s'
        results = connectToMySQL(db).query_db(sql, {'id': user_id})
        return cls(results[0])

    @classmethod
    def update_recipe(cls, data):
        sql = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under = %(under)s WHERE id = %(id)s'
        result = connectToMySQL(db).query_db(sql, data)
        return result

    @classmethod
    def delete_recipe(cls, id):
        sql = 'DELETE FROM recipes WHERE id = %(id)s'
        return connectToMySQL(db).query_db(sql, {'id': id})

    @classmethod
    def get_recipes_with_users(cls):
        sql = 'SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id'
        results = connectToMySQL(db).query_db(sql)
        all_recipes = []
        for r in results:
            recipes = cls(r)
            user_data = {
                'id': r['users.id'],
                'first_name': r['first_name'],
                'last_name': r['last_name'],
                'email': r['email'],
                'password': None,
                'created_at' : r['users.created_at'],
                'updated_at' : r['users.updated_at']
            }
            recipes.user = user_model.User(user_data)
            all_recipes.append(recipes)
        return all_recipes

    @classmethod
    def get_one_recipe_by_id(cls, recipe_id):
        sql = 'SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;'
        data = {
            'id': recipe_id
        }
        results = connectToMySQL(db).query_db(sql, data)
        pprint.pprint(results, sort_dicts=False)
        recipe = cls(results[0])
        user_dict = {
            'id': results[0]['users.id'],
            'first_name': results[0]['first_name'],
            'last_name': results[0]['last_name'],
            'email': results[0]['email'],
            'password': None,
            'created_at' : results[0]['users.created_at'],
            'updated_at' : results[0]['users.updated_at'],
            }

        user_object = user_model.User(user_dict)
        recipe.user = user_object
        return recipe