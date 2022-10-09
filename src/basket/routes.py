import re
import string
from typing import List, Optional, Dict, Union
from flask import request, render_template, session, flash, current_app, redirect, url_for, jsonify
from pydantic import BaseModel, validator, ValidationError
from src.models import Recipe, IngredientRecipe, Basket
from src import database as db
from sqlalchemy.exc import IntegrityError
from . import baskets_blueprint
from .forms import BasketForm
import click
from src.unit_converter.unit_converter import Units

################################
# Helper Function to list out Ingredients from Multiple Recipes
################################

def aggregate_ingredients(basket_recipes):
    uc = Units()
    agg_ingredients_dict = {}
    for item in basket_recipes:
        for ingredient_item in item.recipe.ing_recipe:
            ingred_name = ingredient_item.ingredients.name
            category_name = ingredient_item.ingredients.category.category
            raw_value = ingredient_item.quantity
            raw_unit = ingredient_item.unit
            #Convert to metric
            metric_values = uc.metric_conversion(raw_value, raw_unit)
            ingredient_quantities = {'quantity': metric_values['quantity'],
                                    'unit' : metric_values['unit'],
                                    'category': category_name,
                                    'recipes': [f"{item.recipe.title}: {metric_values['quantity']}{metric_values['unit']}"] 
                                    }
            if ingred_name in agg_ingredients_dict:
                agg_ingredients_dict[ingred_name]['quantity'] += ingredient_quantities['quantity']
                agg_ingredients_dict[ingred_name]['recipes'].append(ingredient_quantities['recipes'][0])
            else:
                agg_ingredients_dict[ingred_name] = ingredient_quantities
    sorted_result = sorted([(k,v) for k, v in agg_ingredients_dict.items()], key=lambda x: (x[1]['category'], x[0]))
    return sorted_result

################################
# Blueprints
################################
@baskets_blueprint.route('/basket', methods=["GET",'POST'])
def list_basket_recipes():
    form = BasketForm()
    current_basket_recipes =  Basket.query.order_by(Basket.id).all()
    agg_ing_dict = aggregate_ingredients(current_basket_recipes)
    if request.method == 'POST':
        try:
            tmp_item = Basket(recipe_id=form.recipe.data,
                            quantity=form.quantity.data
                            )
            db.session.add(tmp_item)
            db.session.commit()
            flash(f'Added {tmp_item.recipe} to basket','success')
            # current_app.logger.info(f'Create new recipe: {new_recipe.title}')
            return redirect(url_for('baskets.list_basket_recipes'))
        except IntegrityError:
            db.session.rollback()
            flash('Error adding recipe to basket','error')

    return render_template('basket_list.html',
                            cbr=current_basket_recipes, agg_ing=agg_ing_dict, form=form)

#Delete a recipe
@baskets_blueprint.route('/basket/remove_recipe/<int:id>', methods=['POST'])
def delete_basket_recipe(id):
    basket_recipe_to_delete = Basket.query.filter_by(recipe_id=id).first()
    db.session.delete(basket_recipe_to_delete)
    db.session.commit()
    flash(f'Removed recipe from basket')
    return redirect(url_for('baskets.list_basket_recipes'))