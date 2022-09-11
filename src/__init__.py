from flask import Flask, render_template, request, session, flash
from pydantic import BaseModel, validator, ValidationError
import logging

#Logging Configuration
file_handler = logging.FileHandler('flask_recipe_app.log')
file_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')  # NEW!
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)

items = ['Apples','Bananas','Carrots']
categories = ['Dairy','Vegetables','Fruit','Grains','Alcohol','Baking','Bakery']
categories_drop_down = [(i,c) for i, c in enumerate(categories)]

class ItemModel(BaseModel):
    "Class for parsing new items in item form"
    item: str
    category: str

    @validator('category')
    def category_check(cls, value):
        if value not in categories:
            raise ValueError(f"Category not in {', '.join(categories)}")
        return value

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.DevConfig')
    app.logger.addHandler(file_handler)
    app.logger.info('Recipe App is Starting...')

    @app.route('/')
    def home():
        return "Hello World"
        # return render_template('items.html',title='Title passed as arg')
    
    @app.route('/items', methods=['GET','POST'])
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
                else:
                    session['items'] = items + [request.form['item']]
                flash(f"{request.form['item']} added to ingredient list!", 'Success')
                return render_template('items.html',items=items, categories=categories, categories_drop_down=categories_drop_down)
            except ValidationError as e:
                flash(f"Ingredient not valid: {e}", "error")
                app.logger.info(f"User tried to input item with category: {request.form['category']}")
        return render_template('items.html',items=items, categories=categories, categories_drop_down=categories_drop_down)

    return app