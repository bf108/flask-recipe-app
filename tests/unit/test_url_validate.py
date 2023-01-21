from src import create_app
import pytest
from src.recipes.forms import BBCUrlForm

def test_url_form():
    app = create_app(config='config.TestConfig')
    with app.app_context():
        form = BBCUrlForm()
        form.url.data = 'some_value'
        assert form.validate() == False
        assert form.errors['url'][0] == 'URL must be https'

        form.url.data = 'www.bbc.co.uk/food/recipes/joes_wow_chicken_38529'
        assert form.validate() == False
        assert form.errors['url'][0] == 'URL must be https'

        form.url.data = 'https://www.bbcgoodfood.co.uk/food/recipes/joes_wow_chicken_38529'
        assert form.validate() == False
        assert form.errors['url'][0] == 'URL must be from www.bbc.co.uk'

        form.url.data = 'https://www.bbc.co.uk/food/recipes/joes_wow_chicken_38529'
        assert form.validate() == True