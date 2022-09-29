from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=120)])
    method = TextAreaField('Method', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Create Recipe')

# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     remember_me = BooleanField('Remember Me')
#     submit = SubmitField('Login')