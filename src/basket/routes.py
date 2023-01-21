import re
import string
from typing import List, Optional, Dict, Union
from flask import request, render_template, session, flash, current_app, redirect, url_for, jsonify
from pydantic import BaseModel, validator, ValidationError
from src.models import Recipe, IngredientRecipe, Basket, BasketRecipes
from src import database as db
from sqlalchemy.exc import IntegrityError
from . import baskets_blueprint
from .forms import BasketForm
import click
from src.unit_converter.unit_converter import UnitConverter

################################
# Helper Function to list out Ingredients from Multiple Recipes
################################

def aggregate_ingredients(basket):
    uc = UnitConverter()
    agg_ingredients_dict = {}
    for basket_recipe in basket.recipes:
        recipe_title = basket_recipe.recipes.title
        multiplier = basket_recipe.quantity
        for ing in basket_recipe.recipes.ingredients:
            item_name = ing.ingredients.name
            item_category = ing.ingredients.category.category
            item_id = ing.ingredient_id
            item_qty = ing.quantity * multiplier
            item_unit = ing.unit
            item_metric = uc.metric_conversion(item_qty, item_unit)

            ingredient_quantities = {'quantity': item_metric['quantity'],
                        'unit' : item_metric['unit'],
                        'category': item_category,
                        'recipes': [f"{recipe_title}: {item_metric['quantity']}{item_metric['unit']}"] 
                        }
            if item_name in agg_ingredients_dict:
                agg_ingredients_dict[item_name]['quantity'] += ingredient_quantities['quantity']
                agg_ingredients_dict[item_name]['recipes'].append(ingredient_quantities['recipes'][0])
            else:
                agg_ingredients_dict[item_name] = ingredient_quantities

    sorted_result = sorted([(k,v) for k, v in agg_ingredients_dict.items()], key=lambda x: (x[1]['category'], x[0]))
    sorted_result = [(i,v) for i, v in enumerate(sorted_result)]
    return sorted_result

################################
# Blueprints
################################
@baskets_blueprint.route('/basket', methods=["GET",'POST'])
def list_basket_recipes():
    form = BasketForm()
    current_basket =  Basket.query.order_by(Basket.id).first()
    agg_ing_dict = aggregate_ingredients(current_basket)
    if request.method == 'POST':
        rec_title = request.form['myRecipe']
        if len(Recipe.query.filter_by(title=rec_title).all()) == 1:
            try:
                rec_id = Recipe.query.filter_by(title=rec_title).first().id
                #If the recipe already exists, then replace value with new
                existing_recipe_in_basket = BasketRecipes.query.filter_by(recipe_id=rec_id).first()
                if existing_recipe_in_basket:
                    existing_recipe_in_basket.quantity = form.quantity.data
                    db.session.commit()
                    flash(f'Updated {rec_title}','success')
                else:
                    tmp_item = BasketRecipes(
                                    basket_id=current_basket.id,
                                    recipe_id=rec_id,
                                    quantity=form.quantity.data
                                    )
                    db.session.add(tmp_item)
                    db.session.commit()
                    flash(f'Added {tmp_item.recipes.title} to basket','success')
                # current_app.logger.info(f'Create new recipe: {new_recipe.title}')
                return redirect(url_for('baskets.list_basket_recipes'))
            except IntegrityError:
                db.session.rollback()
                flash('Error adding recipe to basket','error')
        else:
            flash('Recipe not found - Please select available recipe','error')
    cbr = current_basket.recipes
    return render_template('basket_list.html',
                            cbr=cbr, agg_ing=agg_ing_dict, form=form)

#Delete a recipe
@baskets_blueprint.route('/basket/remove_recipe/<int:id>', methods=['POST'])
def delete_basket_recipe(id):
    basket_recipe_to_delete = BasketRecipes.query.filter_by(recipe_id=id).first()
    db.session.delete(basket_recipe_to_delete)
    db.session.commit()
    flash(f'Removed recipe from basket')
    return redirect(url_for('baskets.list_basket_recipes'))