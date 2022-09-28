from . import users_blueprint
from src.models import User
from flask import render_template, flash, abort, request, current_app, redirect, url_for, escape
from .forms import RegistrationForm, LoginForm
from src import database as db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

@users_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                new_user = User(
                    email=form.email.data,
                    password_plaintext=form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash(f'Registered {new_user.email}!','success')
                current_app.logger.info(f'Registered new user: {new_user.email}')
                return redirect(url_for('ingredients.list_items'))
            except IntegrityError:
                db.session.rollback()
                flash(f'Email {form.email.data} already exists.', 'error')

        else:
            flash('Error in form!','error')
    return render_template('register.html', form=form)

@users_blueprint.route('/login',methods=['GET','POST'])
def login():
    #Check if user is already logged in
    if current_user.is_authenticated:
        flash('Already logged in!')
        return redirect(url_for('ingredients.list_items'))

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            #If email in db then check password correct
            user = User.query.filter_by(email=form.email.data).first()
            #Check password
            if user and user.is_password_correct(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash(f'Thanks for logging in {user.email}!')
                return redirect(url_for("ingredients.list_items"))
        flash('Error with login credentials!','error')
    return render_template('login.html',form=form)

@users_blueprint.route('/logout',methods=['GET'])
@login_required
def logout():
    current_app.logger.info(f"Logging out user: {current_user.email}")
    logout_user()
    flash("Goodbye")
    return redirect(url_for('users.login'))

#Dummy route to test XSS Attack. Injecting URL or JS
#Use of escape parameter from flask prevents any text being executed as code.
@users_blueprint.route('/print_path/<string:path>',methods=['GET'])
def print_path(path):
    return f"<h1>Path provided {escape(path)}!</h1>" 