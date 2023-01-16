from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from src.models import Ingredient, Category
from src import database as db
from src.unit_converter.unit_converter import UnitType
from urllib.parse import urlparse
import re

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
    unit = SelectField('Units', validators=[DataRequired()], choices=UnitType.ALL_UNITS)

class BBCUrlForm(FlaskForm):
    url = StringField('url', validators=[DataRequired()])

    def validate_url(form, field):
        "Custom Validator for URL"
        res = urlparse(field.data)
        scheme, netloc = res.scheme, res.netloc
        if scheme != 'https':
            raise ValidationError('URL must be https')
        if netloc == "":
            raise ValidationError('Invalid URL')
        if netloc != 'www.bbc.co.uk':
            raise ValidationError('URL must be from www.bbc.co.uk')

