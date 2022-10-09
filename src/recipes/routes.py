import re
import string
from typing import List, Optional, Dict, Union
from flask import request, render_template, session, flash, current_app, redirect, url_for, jsonify
from pydantic import BaseModel, validator, ValidationError
from src.models import Ingredient, Category, Recipe, IngredientRecipe
from src import database as db
from sqlalchemy.exc import IntegrityError
from . import recipes_blueprint
from .forms import RecipeForm, IngredientRecipeForm
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
    return render_template('recipe_list.html',
                            recipes=recipes, form=form)

@recipes_blueprint.route('/recipes/<string:title>', methods=["GET",'POST'])
def recipe_detail(title):
    title = title.title()
    form = IngredientRecipeForm()
    recipe_item = Recipe.query.filter_by(title=title).first_or_404()
    list_ingredients = recipe_item.ing_recipe
    table_list = []
    for item in list_ingredients:
        tmp_ing = Ingredient.query.filter_by(id=item.ingredient_id).first_or_404()
        table_list.append({
        'ingredient':tmp_ing,
        'quantity':item.quantity,
        'unit':item.unit
        })

    if request.method == 'POST':
        new_ing_recipe_row = IngredientRecipe(
            recipe_id=recipe_item.id,
            ingredient_id=form.ingredient_id.data,
            quantity=form.quantity.data,
            unit = form.unit.data
        )
        db.session.add(new_ing_recipe_row)
        db.session.commit()
        new_ing = Ingredient.query.filter_by(id=new_ing_recipe_row.ingredient_id).first_or_404()
        flash(f'Added new ingredient: {new_ing.name} to {title}','success')
        return redirect(url_for('recipes.recipe_detail',title=title))
    
    return render_template('recipe_fill.html', recipe=recipe_item, form=form, table_list=table_list)

@recipes_blueprint.route('/recipes/<string:title>/update/<int:id>', methods=["GET",'POST'])
def recipe_update(title, id):
    rec = Recipe.query.filter_by(title=title).first_or_404()
    rec_ing = rec.ing_recipe
    rec_ing_row = [ri for ri in rec_ing if ri.ingredient_id == id][0]
    form = IngredientRecipeForm(obj=rec_ing_row)
    if request.method == 'POST':
        #Form values
        rec_ing_row.quantity = form.quantity.data
        rec_ing_row.unit = form.unit.data
        db.session.commit()
        flash(f'Updated {rec_ing_row.ingredient} in {rec_ing_row.recipe} to {rec_ing_row.quantity}{rec_ing_row.unit}','success')
        return redirect(url_for('recipes.recipe_detail',title=title))
    return render_template('recipe_update.html', recipe_ing=rec_ing_row, title=title, id=id, form=form)

# Route to serve up ingredients for js
@recipes_blueprint.route('/<int:category>/ingredients', methods=["GET"])
def recipe_categories_ingredients(category):
    cat_id = Category.query.filter_by(id=category).first().id
    return jsonify({ing.id: ing.name for ing in Ingredient.query.filter_by(category_id=cat_id).all()})

#Delete an ingredient from a recipe
@recipes_blueprint.route('/recipes/<string:title>/delete/<int:id>', methods=["GET"])
def delete_recipe_ingredient(title, id):
    rec = Recipe.query.filter_by(title=title).first_or_404()
    rec_ing = rec.ing_recipe
    rec_ing_row = [ri for ri in rec_ing if ri.ingredient_id == id][0]
    ing_to_delete = rec_ing_row.ingredient
    db.session.delete(rec_ing_row)
    db.session.commit()
    flash(f'Deleted: {ing_to_delete} from {title}')
    return redirect(url_for('recipes.recipe_detail',title=title))

#Delete a recipe
@recipes_blueprint.route('/recipes/delete/<int:id>', methods=['POST'])
def delete_recipe(id):
    rec_to_delete = Recipe.query.filter_by(id=id).first_or_404()
    db.session.delete(rec_to_delete)
    db.session.commit()
    flash(f'Deleted: {rec_to_delete.title}')
    return redirect(url_for('recipes.list_recipes'))