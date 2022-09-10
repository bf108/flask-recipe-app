import pytest
from src import ItemModel

class TestItemValidation:
    def test_valid_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN valid data passed in
        THEN check validation successful 
        """
        test_item = ItemModel(
                item='Cheese',
                category='Dairy')

        assert test_item.item == 'Cheese'
        assert test_item.category == 'Dairy'

    def test_invalid_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data passed in
        THEN check validation raises ValueError 
        """
        with pytest.raises(ValueError):
            test_bad_item = ItemModel(
                item='Cheese',
                category='Poultry')