# from runner import app

def test_home_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Hello World' in response.data

def test_item_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/items' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/items')
    assert response.status_code == 200
    assert b'Recipe App' in response.data
    assert b'Add a new item' in response.data
    assert b'Food Category: <em>(required)</em>' in response.data
    assert b'Item: <em>(required)</em>' in response.data

def test_post_item_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/items' page is posted to (POST)
    THEN check the valid item is added
    """
    response = test_client.post('/items',
                                data={'item':'Mango','category':'Fruit'})
    assert response.status_code == 200
    assert b'Recipe App' in response.data
    assert b'Add a new item' in response.data
    assert b'Mango' in response.data
    assert b'Food Category:' in response.data
    assert b'Item: <em>(required)</em>' in response.data


def test_actual_duplicate_ingredient(test_client):
    """
    GIVEN a function to query db for dubplicates
    WHEN a duplicate ingredient is passed in
    THEN ckeck tuple returned to confirm duplicate and the value it is duplicate with
    """
    response = test_client.post('/items',
                                data={'item':'Orange','category':'Fruit'})
    assert response.status_code == 200
    assert b'Recipe App' in response.data
    assert b'Ingredient already exists: orange' in response.data

def test_actual_duplicate_ingredient_plural(test_client):
    """
    GIVEN a function to query db for dubplicates
    WHEN a duplicate ingredient is passed in
    THEN ckeck tuple returned to confirm duplicate and the value it is duplicate with
    """
    response = test_client.post('/items',
                                data={'item':'Oranges','category':'Fruit'})
    assert response.status_code == 200
    assert b'Recipe App' in response.data
    assert b'Ingredient already exists: orange' in response.data

def test_actual_duplicate_ingredient_case_insensitive(test_client):
    """
    GIVEN a function to query db for dubplicates
    WHEN a duplicate ingredient is passed in
    THEN ckeck tuple returned to confirm duplicate and the value it is duplicate with
    """
    response = test_client.post('/items',
                                data={'item':'ORANGES','category':'Fruit'})
    assert response.status_code == 200
    assert b'Recipe App' in response.data
    assert b'Ingredient already exists: orange' in response.data

    response = test_client.post('/items',
                                data={'item':'oranges','category':'Fruit'})
    assert response.status_code == 200
    assert b'Recipe App' in response.data
    assert b'Ingredient already exists: orange' in response.data

#Test for non duplicate ingredient in DB Sushi Rice
def test_ingredient_with_punctuation(test_client):
    """
    GIVEN a function to query db for dubplicates
    WHEN a non-duplicate ingredient is passed in
    THEN ckeck the tuple returned to confirm non-duplicate and None
    """
    #Check that it doesn't match with Rice which is in DB
    response = test_client.post('/items',
                                data={'item':'Sushi, Rice!','category':'Grains'})
    assert response.status_code == 200
    assert b'Ingredient should be text only' in response.data

    response = test_client.post('/items',
                                data={'item':'Sushi16 Rice1','category':'Grains'})
    assert response.status_code == 200
    assert b'Ingredient should be text only' in response.data