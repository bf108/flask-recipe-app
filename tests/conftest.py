import pytest
from flask import current_app
from src import create_app
from src.models import Category, Ingredient, User, Recipe
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
    new_user = User('johndoe@some_mail.com',  'FooBar123!')
    return new_user

@pytest.fixture(scope='module')
def new_recipe():
    new_recipe_item = Recipe('Beans on Toast',  'Make it')
    return new_recipe_item

#This fixture is used for registered user e.g login, logout
@pytest.fixture(scope='module')
def register_default_user(test_client):
    test_client.post('/register',
                data={'email':'jane@doe.com','password':'FooBar123!'},
                follow_redirects=True)

#this fixture is used when testing actions on a logged in user
@pytest.fixture(scope='function')
def login_registered_user(test_client, register_default_user):
    test_client.post('/login',
                    data={'email':'jane@doe.com','password':'FooBar123!'},
                    follow_redirects=True)
    
    yield #Where testing happens

    test_client.get('/logout', follow_redirects=True)

