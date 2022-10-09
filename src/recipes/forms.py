from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Optional
from src.models import Ingredient, Category
from src import database as db
from src.unit_converter.unit_converter import Units

def ingredient_choices():
    # return [(ing.id, ing.name) for ing in db.session.query(Ingredient).all()]
    return [(ing.id, ing.name) for ing in Ingredient.query.order_by(Ingredient.id).all()]

def category_choices():
    # return [(ing.id, ing.name) for ing in db.session.query(Ingredient).all()]
    return [(ing.id, ing.category) for ing in Category.query.order_by(Category.id).all()]


#Units for ingredients
class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=120)])
    method = TextAreaField('Method', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Create Recipe')

class IngredientRecipeForm(FlaskForm):
    category_id = SelectField('Category', validators=[DataRequired()], choices=category_choices)
    ingredient_id = SelectField('Ingredient', validators=[DataRequired()], choices=ingredient_choices)
    quantity = FloatField('Qty',validators=[DataRequired()])
    unit = SelectField('Units', validators=[DataRequired()], choices=Units.ALL_UNITS)
