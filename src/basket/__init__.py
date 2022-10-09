"""
The baskets blueprint handles the basket for this  application.
"""
from flask import Blueprint

baskets_blueprint = Blueprint('baskets', __name__, template_folder='templates')

from . import routes