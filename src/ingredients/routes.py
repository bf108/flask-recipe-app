import re
import string
from typing import List, Optional, Dict, Union
from flask import request, render_template, session, flash, current_app, redirect, url_for
from pydantic import BaseModel, validator, ValidationError
from src.models import Ingredient, Category
from src import database
from . import ingredients_blueprint
import click

################################
# Helper Functions for Form Validation
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

def normalize_existing_items(value: List[str]) -> List[str]:
    return [v.lower() for v in value]

def validate_text_only(value: str) -> str:
    "Helper function to validate input text for no digits/punctuation"
    punc_str = "".join(string.punctuation.split('-'))
    if re.search('\d',value) or re.search(f'[{punc_str}]',value):
        raise ValueError("Ingredient should be text only")
    return value.strip().lower()

def check_for_duplicate(value: str, values: Union[str, List]) -> str:
    stems_to_check = find_stems(value)
    for item in values.get('existing',[]):
        if item in stems_to_check:
            raise ValueError(f"Already exists: {item}")
    return value

class CategoryModel(BaseModel):
    "Class for parsing new categories"
    existing: List[str]
    category: str

    _normalize_exisiting = validator('existing', allow_reuse=True)(normalize_existing_items)
    _validate_category = validator('category', allow_reuse=True)(validate_text_only)
    _validatate_duplicate_category = validator('category', allow_reuse=True)(check_for_duplicate)

class ItemModel(BaseModel):
    "Class for parsing new items in item form"
    existing: List
    item: str
    category: str
        
    _normalize_exisiting = validator('existing', allow_reuse=True)(normalize_existing_items)
    _validate_category = validator('item', allow_reuse=True)(validate_text_only)
    _validatate_duplicate_item = validator('item', allow_reuse=True)(check_for_duplicate)

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
# CLI Commands
# These commands will be accessible via: flask --app runner.py ingredients
################################

# Dummy items to show before DB is created
food_groups = {'Dairy':['Milk','Butter','Single Cream','Double Cream', 'Yogurt'],
    'Cheese': ['Cheddar', 'Halloumi', 'Feta', 'Gouda', 'Gruyer', 'Parmesan'],
    'Vegetables': ['Aubergine','Carrot','Courgette','Potato','Pepper','Leeks'],
    'Fruit': ['Apples','Bananas'],
    'Grains': ['Rice','Spaghetti','Gnocci'],
    'Alcohol': ['Red Wine','White Wine','Beer'],
    'Baking': ['Self Raising Flour','Plain Flour','Eggs','Baking Soda'],
    'Bakery': ['Bread','Baguette','Short Crust Pastry', 'Pain-au-chocolate'],
    'Condiments': ['Salt','Black Pepper','Ketchup','Mayonaise'],
    'Meat': ['Chicken Fillets','Beef Mince','Stewing Beef','Bacon'],
    'Fish': ['Salmon','Tuna'],
    'Shell Fish': ['Prawns','Lobster','Mussels'],
    }

@ingredients_blueprint.cli.command('create_default_categories_set')
def create_default_category():
    #Create default food category types
    categories_ = [Category(k) for k in food_groups]
    for c in categories_:
        database.session.add(c)
    database.session.commit()

@ingredients_blueprint.cli.command('create_category')
@click.argument('category')
def create_cateogry(category):
    #Create a new category from CLI
    new_cateogry = Category(category)
    database.session.add(new_cateogry)
    database.session.commit()

@ingredients_blueprint.cli.command('create_default_ingredient_set')
def create_default_ingredients():
    #Create default food ingredient types
    # ingredients_ = [Ingredient(v, k) for k, v in food_groups.items()]
    ingredients_ = []
    for k, cat_ingredients in food_groups.items():
        cat_id = Category.query.filter_by(category=k).first().id
        for i in cat_ingredients:
            ingredients_.append(Ingredient(name=i, category_id=cat_id))
    for c in ingredients_:
        database.session.add(c)
    database.session.commit()

@ingredients_blueprint.cli.command('create_ingredient')
@click.argument('name')
@click.argument('category_id')
def create_ingredient(name, category_id):
    #Create a new ingredient from CLI
    new_ingredient = Ingredient(name, category_id)
    database.session.add(new_ingredient)
    database.session.commit()

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
            new_item_data = ItemModel(existing = current_list_ingredients,
                                      item = request.form.get('item'),
                                      category = request.form.get('category'))
            new_ingredient = Ingredient(new_item_data.item, new_item_data.category)
            database.session.add(new_ingredient)
            database.session.commit()
            flash(f"{new_ingredient.name} added to ingredient list in DB!", 'Success')
            current_app.logger.info(f"New Ingedient Added to SQLite DB: {repr(new_ingredient)}")
            ingredient_list, category_list, categories_drop_down = get_ingredient_category_tuple()
            return render_template('items.html',
                                    items=ingredient_list,
                                    categories=category_list,
                                    categories_drop_down=categories_drop_down)
        except ValidationError as e:
            if not request.form.get('category'):
                flash('Category required','error')
            else:
                flash(str(e).split('item')[1].split('(type=value_error)')[0], 'error')
    ingredient_list, category_list, categories_drop_down = get_ingredient_category_tuple()
    return render_template('items.html',
                            items=ingredient_list,
                            categories=category_list, 
                            categories_drop_down=categories_drop_down)

@ingredients_blueprint.route('/items/update/<int:id>', methods=["GET",'POST'])
def update_item(id):

    #Need to resolve conflicts with duplicats when updating
    #Need to ensure that all ingredients are stored in lowercase

    ing_to_update = Ingredient.query.filter_by(id=id).first_or_404()
    original_item = ing_to_update.name
    original_cat = ing_to_update.category
    original_cat_id = ing_to_update.category.id
    if request.method == 'POST':
        #Remove current ingredient to prevent duplicate alert
        current_list_ingredients = [ing.name for ing in get_list_ingredients() if ing.name != original_item]
        try:
            new_item_data = ItemModel(existing = current_list_ingredients,
                                      item = request.form['item'],
                                      category = request.form['category'])
            ing_to_update.name = new_item_data.item 
            ing_to_update.category_id = new_item_data.category
            database.session.commit()
            flash(f'Updated {original_item} {original_cat} to {ing_to_update}')
            return redirect(url_for('ingredients.list_items'))
        except ValidationError as e:
            flash(str(e).split('item')[1].split('(type=value_error)')[0], 'error')
    #Get categories for drop down
    categories_drop_down = get_category_drop_list()
    #Order so current Category selection is first
    for tup in categories_drop_down:
        if tup[0] == original_cat_id:
            print('found match')
            tmp_cat_tup = [tup]
            categories_drop_down.remove(tup)
    
    modified_drop_down = tmp_cat_tup + categories_drop_down

    return render_template('item_update.html', item=ing_to_update, categories_drop_down=modified_drop_down)


@ingredients_blueprint.route('/categories', methods=['GET','POST'])
def list_categories():
    if request.method == 'POST':
        current_list_categories = [cat.category for cat in get_list_categories()]
        try:
            new_category_data = CategoryModel(existing = current_list_categories,
                                      category = request.form['category_name'])
            new_category = Category(new_category_data.category)
            database.session.add(new_category)
            database.session.commit()
            flash(f"{new_category.category} added to category list in DB!", 'Success')
            category_list, categories_drop_down = get_cat_tuple()
            return render_template('categories.html',
                                category_list=category_list,
                                categories_drop_down=categories_drop_down)

        except ValidationError as e:
            flash(f"""{str(e).split('category')[1].split('(type=value_error)')[0]}""", "error")
            current_app.logger.info(f"User tried to input category: {request.form['category_name']}")
    category_list, categories_drop_down = get_cat_tuple()
    return render_template('categories.html', 
                            category_list=category_list,
                            categories_drop_down=categories_drop_down)

@ingredients_blueprint.route('/categories/delete/<int:id>', methods=['GET'])
def delete_category(id):
    cat_to_delete = Category.query.filter_by(id=id).first_or_404()
    database.session.delete(cat_to_delete)
    database.session.commit()
    flash(f'Deleted: {cat_to_delete.category}')
    return redirect(url_for('ingredients.list_categories'))

@ingredients_blueprint.route('/items/delete/<int:id>', methods=['GET'])
def delete_item(id):
    item_to_delete = Ingredient.query.filter_by(id=id).first_or_404()
    database.session.delete(item_to_delete)
    database.session.commit()
    flash(f'Deleted: {item_to_delete.name}')
    return redirect(url_for('ingredients.list_items'))