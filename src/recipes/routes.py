import re
import string
from typing import List, Optional, Dict, Union
from flask import request, render_template, session, flash, current_app, redirect, url_for, jsonify
from pydantic import BaseModel, validator, ValidationError
from src.models import Ingredient, Category, Recipe, IngredientRecipe, RecipeMethod
from src import database as db
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user
from . import recipes_blueprint
from .forms import RecipeForm, IngredientRecipeForm
import click

################################
# CLI Commands
# These commands will be accessible via: flask --app runner.py ingredients
################################

# Dummy items to show before DB is created
units_options = ['n/a', 'g', 'ml', 'tsp', 'tbsp', 'cup', 'fl oz', 'pint', 'ounce', 'lb']
units_mappings = {i:u for i,u in enumerate(units_options)}
units_selector = [(str(i),u) for i, u in enumerate(units_options)]

def extract_recipe_details_from_form(request):
    """
    logic to create a recipe, method and ingredients from form
    helper function to avoid duplicate codde in add_recipe and update_recipe routes
    """
    recipe_title = request.form['recipeTitle'].lower()
    steps, ingredients, steps, units, qtys = {}, {}, {}, {}, {}
    for k in request.form:
        if k not in ['recipeTitle','csrf_token','myIngredient']:
            num = k.split("_")[-1]
            if 'step' in k:
                steps[num] = request.form[k]
            elif 'unit' in k:
                units[num] = units_mappings[int(request.form[k])]
            elif 'quantity' in k:
                qtys[num] = request.form[k]
            elif 'ingredient' in k:
                ingredients[num] = request.form[k]
    #Ingredient
    #List tuples dict
    ingredients_list = []
    for k, _ in units.items():
        ingredients_list.append({'item':ingredients[k],
                                'quantity':qtys[k],
                                'unit': units[k],
                                'num': k
                                })
    #Steps: List tuples (int, str)
    steps = sorted([(k,v) for k, v in steps.items()], key=lambda x: x[0])

    return recipe_title, steps, ingredients_list

def create_new_recipe(db, recipe_title, steps, ingredients_list, update=False):
    try:
        new_rec = Recipe(title=recipe_title)
        db.session.add(new_rec)
        db.session.commit()
        #Add recipe steps
        recipe_id = Recipe.query.filter_by(title=new_rec.title).first().id
        for s in steps:
            new_step = RecipeMethod(step=s[1], recipe_id=recipe_id)
            db.session.add(new_step)
        db.session.commit()
        #Add ingredients
        for i in ingredients_list:
            ing_id = Ingredient.query.filter_by(name=i['item']).first().id
            new_ing_rec = IngredientRecipe(recipe_id=recipe_id,
                                            ingredient_id=ing_id,
                                            quantity=i['quantity'],
                                            unit=i['unit'])
            db.session.add(new_ing_rec)
        db.session.commit()
        if update:
            flash(f"Updated recipe: {recipe_title}. Steps: {len(steps)}. Ingredients: {len(ingredients_list)}")
        else:
            flash(f"Created recipe: {recipe_title}. Steps: {len(steps)}. Ingredients: {len(ingredients_list)}")
        recipes = Recipe.query.order_by(Recipe.title).all()
        return render_template('recipe_list.html', recipes=recipes)

    except Exception as e:
        print(e)
        db.session.rollback()
        flash(f"Recipe already exists",'error')
        return render_template('recipe_create.html', recipe_title=recipe_title, steps=steps, ingredients=ingredients_list, units=units_selector, update=update)

################################
# Blueprints
################################
@recipes_blueprint.route('/add_recipe', methods=["GET",'POST'])
@login_required
def add_recipe():
    if request.method == 'POST':
        recipe_title, steps, ingredients_list = extract_recipe_details_from_form(request)
        return create_new_recipe(db, recipe_title, steps, ingredients_list)
    else:
        return render_template('recipe_create.html')

@recipes_blueprint.route('/update_recipe/<int:id>', methods=["GET",'POST'])
@login_required
def update_recipe(id):
    if request.method == 'POST':
        recipe_title, steps, ingredients_list = extract_recipe_details_from_form(request)
        #Delete current recipe
        rec_to_delete = Recipe.query.filter_by(title=recipe_title).first()
        print(rec_to_delete)
        db.session.delete(rec_to_delete)
        db.session.commit()
        return create_new_recipe(db, recipe_title, steps, ingredients_list, update=True)
    else:
        rec_to_update = Recipe.query.filter_by(id=id).first()
        recipe_title = rec_to_update.title
        steps = [(i+1,s.step) for i, s in enumerate(rec_to_update.steps)]
        ingredients_list = []
        for k, i in enumerate(rec_to_update.ingredients):
            ingredients_list.append(
            {'item': i.ingredients.name,
            'quantity':i.quantity,
            'unit': i.unit,
            'num': k
            })
        
        return render_template('recipe_create.html', recipe_title=recipe_title, steps=steps, ingredients=ingredients_list, units=units_selector, update=True, id=id)

@recipes_blueprint.route('/', methods=["GET",'POST'])
@login_required
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

@recipes_blueprint.route('/recipes/<int:id>', methods=["GET"])
@login_required
def recipe_detail(id):
    rec_to_view = Recipe.query.filter_by(id=id).first()
    recipe_title = rec_to_view.title
    steps = [(i+1,s.step) for i, s in enumerate(rec_to_view.steps)]
    ingredients_list = []
    for k, i in enumerate(rec_to_view.ingredients):
        ingredients_list.append(
        {'item': i.ingredients.name,
        'quantity':i.quantity,
        'unit': i.unit,
        'num': k
        })
    
    return render_template('recipe_detail.html', recipe_title=recipe_title, steps=steps, ingredients=ingredients_list, units=units_selector, update=True, id=id)

# Route to serve up ingredients for js
@recipes_blueprint.route('/<int:category>/ingredients', methods=["GET"])
def recipe_categories_ingredients(category):
    cat_id = Category.query.filter_by(id=category).first().id
    return jsonify({ing.id: ing.name for ing in Ingredient.query.filter_by(category_id=cat_id).all()})

#Delete a recipe
@recipes_blueprint.route('/recipes/delete/<int:id>', methods=['GET'])
def delete_recipe(id):
    rec_to_delete = Recipe.query.filter_by(id=id).first_or_404()
    db.session.delete(rec_to_delete)
    db.session.commit()
    flash(f'Deleted: {rec_to_delete.title}')
    return redirect(url_for('recipes.list_recipes'))


