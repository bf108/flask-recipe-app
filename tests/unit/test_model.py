#Using the fixture created in conftest.py
def test_category(new_category):
    """
    GIVEN a Category model
    WHEN a new Category object is created
    THEN check attributes are correct: category
    """
    assert new_category.category == 'fruit'

def test_ingredient(new_ingredient):
    """
    GIVEN an Ingredient model
    WHEN a new Ingredient object is created
    THEN check attributes are correct: name, category_id
    """
    assert new_ingredient.name == 'orange'
    assert new_ingredient.category_id == 1

def test_user(new_user):
    """
    GIVEN a User Mode
    WHEN a new User object is created
    THEN check attributes are correct: name, password
    """
    assert new_user.email == 'johndoe@some_mail.com'
    #Check that password has been hashed and therefore not the same
    assert new_user.hashed_password != 'FooBar123!'

def test_new_recipe(new_recipe):
    """
    GIVEN a Recipe Model
    WHEN a new Recipe object is created
    THEN check attributes are correct: title, method
    """
    assert new_recipe.title == 'Beans on Toast'
    #Check that password has been hashed and therefore not the same
    assert new_recipe.method == 'Make it'