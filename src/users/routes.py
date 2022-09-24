from . import users_blueprint
from src.models import User
from flask import render_template, flash, abort, request, current_app, redirect, url_for
from .forms import RegistrationForm
from src import database as db
from sqlalchemy.exc import IntegrityError

@users_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                new_user = User(
                    name=form.name.data,
                    email=form.email.data,
                    password_plaintext=form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash(f'Registered {new_user.email}!','success')
                current_app.logger.info(f'Registered new user: {new_user.email}')
                return redirect(url_for('ingredients.list_items'))
            except IntegrityError:
                db.session.rollback()
                flash(f'ERROR! Email {form.email.data} already exists.', 'error')

        else:
            flash('Error in form!','error')
    return render_template('register.html', form=form)

            