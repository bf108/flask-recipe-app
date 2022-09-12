import logging
from flask import Flask, render_template, request, session, flash
from pydantic import BaseModel, validator, ValidationError

################################
# Helper Functions
################################

def configure_logging(app):
    """
    Define logging format and level in app
    """
    file_handler = logging.FileHandler('flask_recipe_app.log')
    file_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]')  # NEW!
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Recipe App is Starting...')

def register_blueprints(app):
    """
    Register blueprints app
    """
    from src.ingredients import ingredients_blueprint
    app.register_blueprint(ingredients_blueprint)

def create_app(config=None):
    """
    Creates an instance of a Flask Application
    args:
        config: str - Specify which config to use for applicatin. Dev, Prod, Test. Default: DevConfig
    """
    app = Flask(__name__, template_folder='templates')
    if not config:
        config = 'config.DevConfig'
    app.config.from_object(config)
    configure_logging(app)
    register_blueprints(app)

    return app