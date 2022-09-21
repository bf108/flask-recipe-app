import pytest
from pydantic import ValidationError
from src.ingredients.routes import ItemModel, find_stems

def test_find_stems():
    """
    GIVEN a function to find stems of word
    WHEN data string passed in
    THEN check it returns expected list of stems 
    """
    assert find_stems('Cabbage') == sorted(['cabbage','cabbages'])
    assert find_stems('Juices') == sorted(['juice','juices'])
    assert find_stems('Potatoes') == sorted(['potato','potatoes'])
    assert find_stems('Grapes') == sorted(['grape','grapes'])

class TestItemValidation:
    def test_valid_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN valid data passed in
        THEN check validation successful 
        """
        test_item = ItemModel(
                existing_items=[],
                item='Cheese',
                category='Dairy')

        assert test_item.item == 'Cheese'
        assert test_item.category == 'Dairy'
    
    def test_valid_item_caps(self):
        """
        GIVEN a helper class to validate item input
        WHEN valid data passed in
        THEN check validation successful and correct format 
        """
        test_item = ItemModel(
                existing_items=[],
                item='EGGS',
                category='Baking')

        assert test_item.item == 'Eggs'
        assert test_item.category == 'Baking'

    def test_valid_item_lower(self):
        """
        GIVEN a helper class to validate item input
        WHEN valid data passed in
        THEN check validation successful and correct format 
        """
        test_item = ItemModel(
                existing_items=[],
                item='eggs',
                category='Baking')

        assert test_item.item == 'Eggs'
        assert test_item.category == 'Baking'

    def test_digit_in_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data passed in with digit
        THEN check validation raises ValueError 
        """
        with pytest.raises(ValueError):
            test_bad_item = ItemModel(
                existing_items=[],
                item='Chee3e',
                category='Dairy')

    def test_punctuation_in_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data passed in with punctuation
        THEN check validation raises ValueError 
        """
        with pytest.raises(ValueError):
            test_bad_item = ItemModel(
                existing_items=[],
                item='Cheese!',
                category='Dairy')

    def test_missing_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data (missing/empty item) passed in
        THEN check validation raises ValidationError 
        """
        with pytest.raises(ValidationError):
            test_bad_item = ItemModel(
                category='Poultry',
                existing_items=[])
    
    def test_missing_category(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data (missing/empty category) passed in
        THEN check validation raises ValidationError
        """
        with pytest.raises(ValidationError):
            test_bad_item = ItemModel(
                item='Bread',
                existing_items=[]
                )

    def test_missing_existing_items(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data (missing existing items) passed in
        THEN check validation raises ValidationError
        """
        with pytest.raises(ValidationError):
            test_bad_item = ItemModel(
                item='Bread',
                category='Bakery',
                )
    
    def test_exact_duplicate_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data (duplicate item) passed in
        THEN check validation raises ValidationError
        """
        with pytest.raises(ValidationError):
            test_bad_item = ItemModel(
                item='Bread',
                category='Bakery',
                existing_items = ['Bread']
                )

    def test_plural_single_duplicate_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data (duplicate item) passed in
        THEN check validation raises ValidationError
        """
        with pytest.raises(ValidationError):
            test_bad_item = ItemModel(
                item='Beans',
                category='Bakery',
                existing_items = ['Bean']
                )

    def test_single_plural_duplicate_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data (duplicate item) passed in
        THEN check validation raises ValidationError
        """
        with pytest.raises(ValidationError):
            test_bad_item = ItemModel(
                item='Banana',
                category='Bakery',
                existing_items = ['Bananas']
                )