"""
The users blueprint handles the user management for this application.
Specifically, this blueprint allows users to register and login/out.
"""
from flask import Blueprint

users_blueprint = Blueprint('users', __name__, template_folder='templates')

from . import routes