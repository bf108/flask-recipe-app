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
class ItemModel(BaseModel):
    "Class for parsing new items in item form"
    item: str
    category: str

    @validator('category')
    def category_check(cls, value):
        if value not in categories:
            raise ValueError(f"Category not in {', '.join(categories)}")
        return value

def check_duplicate_ingredient(new_input_ingredient):
    """
    Check for ingredient in db before adding case insensitive search.
    Will also perform regex search for similar ingredients
    e.g Orange vs Oranges
    """
    #Check ingredient is singular:
    alt_input = new_input_ingredient
    if new_input_ingredient.endswith('oes'):
        alt_input = new_input_ingredient[:-2]
    elif new_input_ingredient.endswith('s'):
        alt_input = new_input_ingredient[:-1]

    base_check = Ingredient.query.filter(Ingredient.name.like(f'{new_input_ingredient}%')).all()
    alt_check = Ingredient.query.filter(Ingredient.name.like(f'{alt_input}%')).all()
    similar_ingredients = list(set(base_check + alt_check))
    for si in similar_ingredients:
        if si.name.lower() in [v.lower() for v in [new_input_ingredient, alt_input]]:
            return (True, si.name)
    return (False, None)


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
        duplicated, ing = check_duplicate_ingredient(request.form['item'])
        if duplicated:
            flash(f"Potential Duplicate with: {ing}", 'error')
            ingredient_list, category_list, categories_drop_down = get_ingredient_category_tuple()
            return render_template('items.html',
                        items=ingredient_list,
                        categories=category_list,
                        categories_drop_down=categories_drop_down)
        else:
            new_ingredient = Ingredient(request.form['item'], request.form['category'])
            database.session.add(new_ingredient)
            database.session.commit()
            flash(f"{new_ingredient.name} added to ingredient list in DB!", 'Success')
            current_app.logger.info(f"New Ingedient Added to SQLite DB: {repr(new_ingredient)}")
            ingredient_list, category_list, categories_drop_down = get_ingredient_category_tuple()
            return render_template('items.html',
                                    items=ingredient_list,
                                    categories=categories,
                                    categories_drop_down=categories_drop_down)
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