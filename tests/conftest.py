import pytest
from flask import current_app
from src import create_app
from src.models import Category, Ingredient, User
from src import database as db

@pytest.fixture(scope='module')
def test_client():
    app = create_app(config='config.TestConfig')
    with app.test_client() as testing_client:
    #Use a content manager to add application to stack 
        with app.app_context():
            #Once stack available you can perform action on application context
            current_app.logger.info('Inside of test_client() fixture...')
            #Context manager handles poppin off content from stack and closing context
            
            #Create the testing database and all necessary tables
            db.create_all()

        #Use yield instead of return
        yield testing_client

        #Empty db after testing
        with app.app_context():
            db.drop_all()

@pytest.fixture(scope='module')
def new_category():
    new_cat = Category('Fruit')
    return new_cat

@pytest.fixture(scope='module')
def new_ingredient():
    new_ingredient = Ingredient('Orange', 1)
    return new_ingredient

@pytest.fixture(scope='module')
def new_user():
    new_user = User('John Doe','johndoe@some_mail.com',  'FooBar123!')
    return new_user