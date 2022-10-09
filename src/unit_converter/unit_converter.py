class Units:
    METRIC = ['n/a','g','ml']
    IMPERIAL = ['tsp','tbsp','cup','fl oz', 'pint','ounce','lb']
    ALL_UNITS = METRIC + IMPERIAL
    def __init__(self):
        self.metric = ['n/a','g','ml','l']
        self.imperial = ['tsp','tbsp','cup','fl oz', 'pint','ounce','lb', 'glass']
        self.all_units = self.metric + self.imperial
        self.conversion_table = {
            'tsp': {'value':5, 'unit':'ml'},
            'tbsp': {'value':15, 'unit':'ml'},
            'cup': {'value':250, 'unit':'ml'},
            'glass': {'value':275, 'unit':'ml'},
            'fl oz': {'value':30, 'unit':'ml'},
            'pint': {'value':575, 'unit':'ml'},
            'ounce': {'value':28, 'unit':'g'},
            'lb': {'value':450, 'unit':'g'},
        }

    def metric_conversion(self, value, unit):
        if unit in self.metric:
            return {'quantity':value, 'unit':unit}
        return {
            'quantity': self.conversion_table[unit]['value'] * value,
            'unit': self.conversion_table[unit]['unit']
        }
            
        


