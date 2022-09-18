import logging
from flask import Flask, render_template, request, session, flash
from pydantic import BaseModel, validator, ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

################################
# Configuration
################################
# Create a naming convention for the database tables
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
database = SQLAlchemy(metadata=metadata)


################################
# Helper Functions
################################

def initialize_extensions(app):
    """
    Since the application instance is now created, pass it to each Flask
    extension instance to bind it to the Flask application instance (app)
    """
    database.init_app(app)

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

def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

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
    initialize_extensions(app)
    configure_logging(app)
    register_blueprints(app)
    register_error_pages(app)
    return app