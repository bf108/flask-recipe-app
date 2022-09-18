"""
The ingredients blueprint handles the user management for this application.
Specifically, this blueprint allows for users to add, edit, and delete
ingredient data.
"""
from flask import Blueprint

ingredients_blueprint = Blueprint('ingredients', __name__, template_folder='templates')

from . import routes