import pytest
from src.unit_converter.unit_converter import Units

def test_units():
    """
    GIVEN a Unit converter object
    WHEN value and unit combintions are passed in
    THEN check it returns expected conversion 
    """
    # Instantiate unit converter object
    uc = Units()
    assert uc.metric_conversion(5,'tsp') == {'quantity':25, 'unit':'ml'}
    assert uc.metric_conversion(2,'tbsp') == {'quantity':30, 'unit':'ml'}
    assert uc.metric_conversion(0.5,'cup') == {'quantity':125, 'unit':'ml'}
    assert uc.metric_conversion(5,'n/a') == {'quantity':5, 'unit':'n/a'}
    assert uc.metric_conversion(5,'ml') == {'quantity':5, 'unit':'ml'}
    assert uc.metric_conversion(5,'g') == {'quantity':5, 'unit':'g'}
    assert uc.metric_conversion(5,'fl oz') == {'quantity':150, 'unit':'ml'}
    assert uc.metric_conversion(2,'pint') == {'quantity':1150, 'unit':'ml'}
    assert uc.metric_conversion(0.25,'lb') == {'quantity':112.5, 'unit':'g'}
