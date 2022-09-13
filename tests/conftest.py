import pytest
from flask import current_app
from src import create_app

@pytest.fixture(scope='module')
def test_client():
    app = create_app(config='config.TestConfig')
    
    with app.test_client() as testing_client:
    #Use a content manager to add application to stack 
        with app.app_context():
            #Once stack available you can perform action on application context
            current_app.logger.info('Inside of test_client() fixture...')
        #Context manager handles poppin off content from stack and closing context

        #Use yield instead of return
        yield testing_client