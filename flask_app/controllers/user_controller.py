from flask import Flask, flash, redirect, render_template, request, session
from flask_app import app
from flask_app.models import user_model, recipe_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def show_registration_page():
    if 'message' in session:
        message = session['message']
        del session['message']
    else:
        message = None
    return render_template('register.html', message = message)


@app.route('/welcome')
def show_welcome_page():
    if 'user_id' not in session:
        return redirect('/')
    user = user_model.User.get_one_user(session['user_id'])
    all_recipes = recipe_model.Recipe.get_recipes_with_users()
    return render_template('welcome.html', user = user, all_recipes = all_recipes)


@app.route('/register', methods=['POST'])
def register():

    valid = user_model.User.validate_user1(request.form)

    if valid:

        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
        }
        id = user_model.User.create_user(data)
        session['user_id'] = id
        return redirect('/welcome')
    else:
        return redirect ('/')


@app.route('/login', methods=['POST'])
def login():
    user = user_model.User.get_user_by_email(request.form)
    if not user:
        flash("Invalid email/password","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid email/password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/welcome')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


