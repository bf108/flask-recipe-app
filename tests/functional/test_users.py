#
def test_get_registration_page(test_client):
    """
    GIVEN a Flask application
    WHEN the '/users/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'User Registration' in response.data
    assert b'Name' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Register' in response.data

def test_post_registration_page_nominal(test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' route is POSTED new valid user details(POST)
    THEN check the response is valid
    """
    response = test_client.post('/register',
                                data={'name':'John Doe', 
                                        'email':'johndoe@email.com',
                                        'password':'some_password'
                                        })
    #Should redirect to Ingredient List page
#     assert b'Registered johndoe@email.com!' in response.data
    assert response.status_code == 302

    #Some checks for redirect to Ingredients Page

def test_post_registration_page_off_nominal(test_client):
    """
    GIVEN a Flask application
    WHEN the '/register' route is POSTED non valid user details(POST)
    THEN check the response is invalid
    """

    #Missing email
    response = test_client.post('/register',
                                data={'name':'John Doe', 
                                        'password':'some_password'
                                        },
                                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Error in form!' in response.data

    #Missing name
    response = test_client.post('/register',
                                data={'email':'johndoe@someemail.com',
                                        'password':'some_password'
                                        },
                                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Error in form!' in response.data

    #Missing password
    response = test_client.post('/register',
                                data={'name':'John Doe', 
                                        'email':'johndoe@someemail.com',
                                        },
                                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Error in form!' in response.data

    #Duplicate USER/EMAIL
    response = test_client.post('/register',
                            data={'name':'John Doe', 
                                    'email':'johndoe@someemail.com',
                                    'password':'some_password'
                                    },
                                    follow_redirects=True)

    response = test_client.post('/register',
                            data={'name':'John Doe', 
                                    'email':'johndoe@someemail.com',
                                    'password':'some_password'
                                    },
                                    follow_redirects=True)
    
    assert response.status_code == 200
    assert b'ERROR! Email johndoe@someemail.com already exists.' in response.data