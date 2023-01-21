from flask_wtf import FlaskForm
from wtforms import  IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange
from src.models import Recipe
from src import database as db

def recipe_choices():
    return sorted([(rec.id, rec.title) for rec in Recipe.query.order_by(Recipe.id).all()],
     key=lambda x: x[1])

class BasketForm(FlaskForm):
    # recipe = SelectField('Recipe', validators=[DataRequired()], choices=recipe_choices)
    quantity = IntegerField('Qty',validators=[DataRequired(), NumberRange(min=1)], default=1)
    submit = SubmitField('Include Recipe')
