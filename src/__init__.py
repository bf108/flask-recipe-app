from flask import Flask, render_template, request, session, flash
from pydantic import BaseModel, validator, ValidationError
import logging

################################
# Helper Functions
################################

def configure_logging(app):
    file_handler = logging.FileHandler('flask_recipe_app.log')
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')  # NEW!
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Recipe App is Starting...')

def register_blueprints(app):
    from src.ingredients import ingredients_blueprint
    app.register_blueprint(ingredients_blueprint)

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object('config.DevConfig')
    configure_logging(app)
    register_blueprints(app)

    return app