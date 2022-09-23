import pytest
from pydantic import ValidationError
from src.ingredients.routes import ItemModel, CategoryModel, find_stems

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

class TestCategoryValidation:
    def test_valid_category(self):
        """
        GIVEN a helper class to validate category input
        WHEN valid data passed in
        THEN check validation successful 
        """
        test_item = CategoryModel(
                existing=[],
                category='Dairy')

        assert test_item.category == 'Dairy'
    
    def test_invalid_category_punc(self):
        """
        GIVEN a helper class to validate category input
        WHEN invalid data passed in
        THEN check validation not successful 
        """

        with pytest.raises(ValueError):
            test_bad_item = CategoryModel(
                existing=[],
                category='Dairy!')

    def test_invalid_category_digit(self):
        """
        GIVEN a helper class to validate category input
        WHEN invalid data passed in
        THEN check validation not successful 
        """

        with pytest.raises(ValueError):
            test_bad_item = CategoryModel(
                existing=[],
                category='Dairy1')
    
    def test_invalid_category_duplicate(self):
        """
        GIVEN a helper class to validate category input
        WHEN invalid data passed in
        THEN check validation not successful 
        """

        with pytest.raises(ValueError):
            test_bad_item = CategoryModel(
                existing=['Dairy'],
                category='Dairy')

class TestItemValidation:
    def test_valid_item(self):
        """
        GIVEN a helper class to validate item input
        WHEN valid data passed in
        THEN check validation successful 
        """
        test_item = ItemModel(
                existing=[],
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
                existing=[],
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
                existing=[],
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
                existing=[],
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
                existing=[],
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
                existing=[])
    
    def test_missing_category(self):
        """
        GIVEN a helper class to validate item input
        WHEN invalid data (missing/empty category) passed in
        THEN check validation raises ValidationError
        """
        with pytest.raises(ValidationError):
            test_bad_item = ItemModel(
                item='Bread',
                existing=[]
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
                existing = ['Bread']
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
                existing = ['Bean']
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
                existing = ['Bananas']
                )