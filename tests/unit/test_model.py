#Using the fixture created in conftest.py
def test_category(new_category):
    """
    GIVEN a Category model
    WHEN a new Category object is created
    THEN check attributes are correct: category
    """
    assert new_category.category == 'Fruit'

def test_ingredient(new_ingredient):
    """
    GIVEN an Ingredient model
    WHEN a new Ingredient object is created
    THEN check attributes are correct: name, category_id
    """
    assert new_ingredient.name == 'Orange'
    assert new_ingredient.category_id == 1
