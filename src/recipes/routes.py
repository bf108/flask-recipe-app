import re
import string
from typing import List, Optional, Dict, Union
from flask import request, render_template, session, flash, current_app, redirect, url_for
from pydantic import BaseModel, validator, ValidationError
from src.models import Ingredient, Category, Recipe
from src import database as db
from sqlalchemy.exc import IntegrityError
from . import recipes_blueprint
from .forms import RecipeForm
import click

################################
# Helper Functions for Form Validation
################################

#

################################
# CLI Commands
# These commands will be accessible via: flask --app runner.py ingredients
################################

# Dummy items to show before DB is created

################################
# Blueprints
################################
@recipes_blueprint.route('/recipes', methods=["GET",'POST'])
def list_recipes():
    form = RecipeForm()
    if request.method == 'POST':
        # current_list_ingredients = [ing.name for ing in get_list_ingredients()]
        try:
            # new_item_data = ItemModel(existing = current_list_ingredients,
            #                           item = request.form['item'],
            #                           category = request.form['category'])
            new_recipe = Recipe(
                title=form.title.data,
                method=form.method.data)
            db.session.add(new_recipe)
            db.session.commit()
            flash(f'Added {new_recipe.title}','success')
            current_app.logger.info(f'Create new recipe: {new_recipe.title}')
            return redirect(url_for('recipes.list_recipes'))
        except IntegrityError:
            db.session.rollback()
            flash('Error creating recipe','error')
    recipes = Recipe.query.order_by(Recipe.id).all()
    return render_template('recipe.html',
                            recipes=recipes, form=form)