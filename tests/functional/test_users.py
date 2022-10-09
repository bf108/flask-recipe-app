#
def test_get_registration_page(test_client):
    """
    GIVEN a Flask test application
    WHEN the '/users/register' page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/register')
    assert response.status_code == 200
    assert b'User Registration' in response.data
    assert b'Email' in response.data
    assert b'Password' in response.data
    assert b'Register' in response.data

def test_post_registration_page_nominal(test_client):
    """
    GIVEN a Flask test application
    WHEN the '/register' route is POSTED new valid user details(POST)
    THEN check the response is valid
    """
    response = test_client.post('/register',
                                data={'email':'johndoe@email.com',
                                        'password':'some_password'
                                        })
    #Should redirect to Ingredient List page
#     assert b'Registered johndoe@email.com!' in response.data
    assert response.status_code == 302

    #Some checks for redirect to Ingredients Page

def test_post_registration_page_off_nominal(test_client):
    """
    GIVEN a Flask test application
    WHEN the '/register' route is POSTED non valid user details(POST)
    THEN check the response is invalid
    """

    #Missing email
    response = test_client.post('/register',
                                data={'password':'some_password'
                                        },
                                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Error in form!' in response.data

    #Missing password
    response = test_client.post('/register',
                                data={'email':'johndoe@someemail.com',
                                        },
                                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Error in form!' in response.data

    #Duplicate USER/EMAIL
    response = test_client.post('/register',
                            data={'email':'johndoe@someemail.com',
                                    'password':'some_password'
                                    },
                                    follow_redirects=True)

    response = test_client.post('/register',
                            data={'email':'johndoe@someemail.com',
                                    'password':'some_password'
                                    },
                                    follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Email johndoe@someemail.com already exists.' in response.data

def test_get_login_page(test_client):
    """
    GIVEN a flask test application
    WHEN GET request made to the '/login' route
    THEN check the page formatted correctly
    """
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'email' in response.data
    assert b'password' in response.data

def test_user_login_logout_successful(test_client, register_default_user):
    """
    GIVEN a Flask test application and a registered user
    WHEN the '/login' route is POSTED valid user details
    THEN check user is logged in successfully
    """
    response = test_client.post('/login',
                                data={'email':'jane@doe.com','password':'FooBar123!'},
                                follow_redirects=True)
    #Redirect after succesful login?
    assert response.status_code == 200 #
    assert b'Thanks for logging in jane@doe.com!' in response.data
    assert b'Login' not in response.data
    
    """
    GIVEN a Flask test application and a registered user
    WHEN the '/logout' route is visited
    THEN check user is logged out successfully
    """
    response = test_client.get('/logout',
                                follow_redirects=True)
    #Redirect after succesful login?
    assert response.status_code == 200 #
    assert b'Login' in response.data
    assert b'email' in response.data
    assert b'password' in response.data

def test_user_login_unsuccessful(test_client, register_default_user):
    """
    GIVEN a Flask test application
    WHEN the '/login' route is POSTED invalid user details(POST)
    THEN check user is logged in
    """
    response = test_client.post('/login',
                                data={'email':'jane@doe.com','password':'BarFoo123!'},# incorrect pw
                                follow_redirects=True)
    #Redirect after succesful login?
    assert response.status_code == 200 #
    assert b'Error with login credentials!' in response.data

def test_user_login_login(test_client, login_registered_user):
    """
    GIVEN a Flask test application
    WHEN the '/login' route is POSTED when user already logged in
    THEN check user is notified of being logged in
    """
    response = test_client.post('/login',
                            data={'email':'jane@doe.com','password':'FooBar123!'},
                            follow_redirects=True)

    assert response.status_code == 200 #
    assert b'Already logged in!' in response.data

def test_invalid_post_request_logout(test_client):
    """
    GIVEN a Flask test application
    WHEN a post request is set to '/logout'
    THEN check method not allowed code is shown: 405
    """
    test_client.post('/login',
                        data={'email':'jane@doe.com','password':'FooBar123!'},
                        follow_redirects=True)

    response = test_client.post('/logout')

    assert response.status_code == 405 #
    assert b'Goodbye' not in response.data
    assert b'Method Not Allowed' in response.data

def test_logout_when_not_logged_in(test_client):
    """
    GIVEN a Flask test application
    WHEN a get request is made on '/logout' route when User not logged in
    THEN check that user notified of not being logged in and redirected to login page
    """
    #Ensure that no user is logged in
    test_client.get('/logout',follow_redirects=True)
    response = test_client.get('/logout', follow_redirects=True)

    assert response.status_code == 200 #
    assert b'Goodbye' not in response.data
    # assert b'Method Not Allowed' in response.data
    assert b'Please log in to access this page.' in response.data

def test_get_recipes_page(test_client):
    """
    GIVEN a flask test application
    WHEN GET request made to the '/recipes' route
    THEN check the page formatted correctly
    """
    response = test_client.get('/recipes')
    assert response.status_code == 200
    assert b'Title' in response.data
    assert b'Method' in response.data
    assert b'Create Recipes' in response.data
    assert b'Create Recipe' in response.data

def test_create_recipes_nominal(test_client):
    """
    GIVEN a flask test application
    WHEN POST request made to the '/recipes' route 
    THEN check the page formatted correctly
    """
    response = test_client.post('/recipes', 
                        data={'title':'Beans on Toast','Method':'Make it'},
                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Added Beans on Toast' in response.data
    assert b'Title' in response.data
    assert b'Method' in response.data
    assert b'Create Recipes' in response.data
    assert b'Create Recipe' in response.data

def test_create_recipes_off_nominal(test_client):
    """
    GIVEN a flask test application
    WHEN POST request made to the '/recipes' route with duplicate recipe
    THEN check the page formatted correctly
    """
    response = test_client.post('/recipes', 
                        data={'title':'Beans on Toast','Method':'Make it'})

    response = test_client.post('/recipes', 
                        data={'title':'Beans on Toast','Method':'Make it'},
                        follow_redirects=True)
    assert response.status_code == 200
    assert b'Error creating recipe' in response.data
    assert b'Title' in response.data
    assert b'Method' in response.data
    assert b'Create Recipes' in response.data
    assert b'Create Recipe' in response.data