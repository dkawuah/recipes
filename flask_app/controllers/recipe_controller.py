from flask import Flask, flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models import recipe_model
from flask_app.models import user_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/create_recipe')
def display_new_recipe_form():
    users = user_model.User.get_all_users()
    return render_template('create_recipe.html', users = users)

@app.route('/view_recipe/<int:recipe_id>')
def view_one_recipe(recipe_id):
    # recipe = recipe_model.Recipe.get_one_recipe(id)
    user = user_model.User.get_one_user(session['user_id'])
    recipe_object = recipe_model.Recipe.get_one_recipe_by_id(recipe_id)
    return render_template('view_recipe.html', recipe = recipe_object, user = user)

@app.route('/recipes/delete/<int:id>')
def delete_one_recipe(id):
    recipe_model.Recipe.delete_recipe(id)
    return redirect('/welcome')

@app.route('/recipes/edit/<int:id>')
def edit_one_recipe(id):
    recipe = recipe_model.Recipe.get_one_recipe(id)
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipes/edit/<int:id>', methods = ['POST'])
def update_one_recipe(id):
    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under': request.form['under'],
        'created_at': request.form['created_at'],
    }
    recipe_model.Recipe.update_recipe(data)
    return redirect (f'/view_recipe/{id}')


@app.route('/create_recipe', methods = ['POST'])
def create_new_recipe():
    data = {
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'under': request.form['under'],
        'user_id': session['user_id'],
    }
    recipe_model.Recipe.create_recipe(data)
    return redirect('/welcome')


@app.route('/back_to_recipes')
def back_to_recipe_page():
    return redirect ('/welcome')

