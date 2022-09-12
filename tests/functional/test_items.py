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


