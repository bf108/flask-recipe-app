import re
import string
from typing import List, Optional
from flask import request, render_template, session, flash, current_app
from pydantic import BaseModel, validator, ValidationError
from src.models import Ingredient, Category
from src import database
from . import ingredients_blueprint

################################
# Dummy items to show before DB is created
################################
items = ['Apples','Bananas','Carrots']
categories = ['Dairy','Vegetables','Fruit','Grains','Alcohol','Baking','Bakery']
categories_drop_down = [(i,c) for i, c in enumerate(categories)]

################################
# Helper Class to Validate New Items
################################
def find_stems(some_ingredient: str) -> List[str]:
    """
    Find stems of word and return list of lowercase stems 
    """
    stems = [some_ingredient]
    if some_ingredient.endswith('oes'):
        stems.append(some_ingredient[:-2])
    elif some_ingredient.endswith('s'):
        stems.append(some_ingredient[:-1])
    else:
        stems.append(f"{some_ingredient}s")
    return sorted([s.lower() for s in stems])

class ItemModel(BaseModel):
    "Class for parsing new items in item form"
    existing_items: List[str]
    item: str
    category: str
        
    #Convert SQLAlchemy query list strings to lowercase string
    @validator('existing_items')
    def normalize_existing_items(cls, value):
        return [v.lower() for v in value]
    
    #Check for digits in item
    @validator('item')
    def item_check_digit(cls, value):
        if re.search('\d',value):
            raise ValueError("Ingredient should be text only")
        return value
    
    #Check for punctuation in item: ONLY allow hyphen "-"
    @validator('item')
    def item_check_punctuation(cls, value):
        punc_str = "".join(string.punctuation.split('-'))
        if re.search(f'[{punc_str}]',value):
            raise ValueError("Ingredient should be text only")
        return value
    
    #Format new ingredient correctly
    @validator('item')
    def normalize_existing_item(cls, value):
        return value.strip().title()
    
    #Check for duplicate ingredient
    @validator('item')
    def item_check_duplicate(cls, value, values, **kwargs):
        stems_to_check = find_stems(value)
        print(stems_to_check)
        for item in values.get('existing_items',[]):
            if item in stems_to_check:
                raise ValueError(f"Ingredient already exists: {item}")
        return value

def check_category_duplicate(new_input_category):
    """
    Check for dubplicates before inserting new category
    case insensitive search in Category table
    """
    return len(Category.query.filter(Category.category.ilike(new_input_category.lower())).all()) > 0

def get_list_ingredients():
    #Helper function to return list of ingredients
    return Ingredient.query.order_by(Ingredient.id).all()

def get_category_drop_list():
    #Simple helper function to create list of tuples (int, str)#
    return [(c.id, c.category) for c in Category.query.order_by(Category.id).all()]

def get_list_categories():
    #Helper function to return list of categories
    return Category.query.order_by(Category.id).all()

def get_cat_tuple():
    #Helper function to return list of categories and drop down list for template
    cat_list = get_list_categories()
    cat_drop_down_list = get_category_drop_list()
    return (cat_list, cat_drop_down_list)

def get_ingredient_category_tuple():
    #Helper function to return list of ingredients, categories and drop down list for template
    ing_list = get_list_ingredients()
    cat_list, cat_dd_list = get_cat_tuple()
    return (ing_list, cat_list, cat_dd_list)

################################
# Blueprints
################################
@ingredients_blueprint.route('/')
def home():
    return "Hello World"

@ingredients_blueprint.route('/items', methods=["GET",'POST'])
def list_items():
    if request.method == 'POST':
        current_list_ingredients = [ing.name for ing in get_list_ingredients()]
        try:
            new_item_data = ItemModel(existing_items = current_list_ingredients,
                                      item = request.form['item'],
                                      category = request.form['category'])
            new_ingredient = Ingredient(new_item_data.item, new_item_data.category)
            database.session.add(new_ingredient)
            database.session.commit()
            flash(f"{new_ingredient.name} added to ingredient list in DB!", 'Success')
            current_app.logger.info(f"New Ingedient Added to SQLite DB: {repr(new_ingredient)}")
            ingredient_list, category_list, categories_drop_down = get_ingredient_category_tuple()
            return render_template('items.html',
                                    items=ingredient_list,
                                    categories=categories,
                                    categories_drop_down=categories_drop_down)
        except ValidationError as e:
            flash(str(e).split('ItemModel\nitem\n')[1].split('(type=value_error)')[0], 'error')
    ingredient_list, category_list, categories_drop_down = get_ingredient_category_tuple()
    return render_template('items.html',
                            items=ingredient_list,
                            categories=category_list, 
                            categories_drop_down=categories_drop_down)

@ingredients_blueprint.route('/categories', methods=['GET','POST'])
def list_categories():
    if request.method == 'POST':
        try:
            new_category = Category(request.form['category_name'])
            if not check_category_duplicate(new_category.category):
                database.session.add(new_category)
                database.session.commit()
                flash(f"{new_category.category} added to category list in DB!", 'Success')
                category_list, categories_drop_down = get_cat_tuple()
                return render_template('categories.html',
                                    category_list=category_list,
                                    categories_drop_down=categories_drop_down)
            else:
                flash(f"{new_category.category} already in DB!", 'error')
                category_list, categories_drop_down = get_cat_tuple()
                return render_template('categories.html', 
                                        category_list=category_list,
                                        categories_drop_down= categories_drop_down)
        except ValidationError as e:
            flash(f"Invalid Category: {e}", "error")
            current_app.logger.info(f"User tried to input category: {request.form['category_name']}")
    category_list, categories_drop_down = get_cat_tuple()
    return render_template('categories.html', 
                            category_list=category_list,
                            categories_drop_down=categories_drop_down)