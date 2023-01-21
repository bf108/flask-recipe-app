class UnitType:
    "ALLOWED UNITS"
    METRIC = ['n/a','g','ml','cm','litre','l',""]
    IMPERIAL = ['tsp','tbsp','cup','fl oz', 'pint','ounce','lb','oz','inch','glass']
    ALL_UNITS = METRIC + IMPERIAL

class UnitConverter:
    # METRIC = ['n/a','g','ml','cm','litre']
    # IMPERIAL = ['tsp','tbsp','cup','fl oz', 'pint','ounce','lb','oz','inch','glass']
    #ALL_UNITS = METRIC + IMPERIAL

    def __init__(self):
        self.metric = UnitType.METRIC
        self.imperial = UnitType.IMPERIAL
        self.all_units = UnitType.ALL_UNITS
        # self.metric + self.imperial
        self.conversion_table = {
            'tsp': {'value':5, 'unit':'ml'},
            'tbsp': {'value':15, 'unit':'ml'},
            'cup': {'value':250, 'unit':'ml'},
            'glass': {'value':275, 'unit':'ml'},
            'fl oz': {'value':30, 'unit':'ml'},
            'oz': {'value':30, 'unit':'ml'},
            'pint': {'value':575, 'unit':'ml'},
            'ounce': {'value':28, 'unit':'g'},
            'lb': {'value':450, 'unit':'g'},
            'inch': {'value': 2.5, 'unit':'cm'},
            'litre': {'value': 1000, 'unit':'ml'},
            'l': {'value': 1000, 'unit':'ml'},
        }

    def metric_conversion(self, value, unit):
        if unit in self.metric and unit not in ['litre','l']:
            if unit == 'n/a':
                return {'quantity':value, 'unit':''}
            else:
                return {'quantity':value, 'unit':unit}
        return {
            'quantity': self.conversion_table[unit]['value'] * value,
            'unit': self.conversion_table[unit]['unit']
        }
            
        


