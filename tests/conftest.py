import pytest
from src import create_app

@pytest.fixture(scope='module')
def test_client():
    app = create_app(config='config.TestConfig')
    testing_client = app.test_client()
    return testing_client