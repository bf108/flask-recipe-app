from flask import request, render_template, session, flash, current_app
from pydantic import BaseModel, validator, ValidationError
import logging
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

################################
# Blueprints
################################
@ingredients_blueprint.route('/')
def home():
    return "Hello World"


@ingredients_blueprint.route('/items', methods=["GET",'POST'])
def list_items():
    if request.method == 'POST':
        print(request.form)
        try:
            category_input = ItemModel(
                    item=request.form['item'],
                    category=request.form['category']
                    )
            if 'items' in session:
                session['items'].append(request.form['item'])
                items.append(request.form['item'])
            else:
                session['items'] = items + [request.form['item']]
                items.append(request.form['item'])
            flash(f"{request.form['item']} added to ingredient list!", 'Success')
            current_app.logger.info(f"New Ingedient Added: {request.form['item']}")
            return render_template('items.html',items=items, categories=categories, categories_drop_down=categories_drop_down)
        except ValidationError as e:
            flash(f"Ingredient not valid: {e}", "error")
            current_app.logger.info(f"User tried to input item with category: {request.form['category']}")
    return render_template('items.html',
                            items=items,
                            categories=categories, 
                            categories_drop_down=categories_drop_down)