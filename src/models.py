from src import database

class Ingredient(database.Model):
    """
    Class that represents an ingredient

    This stores the following attributes
        name: (type: string)
        category: (type: string)
    """

    __tablename__ = 'ingredients'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, nullable=False)
    category = database.Column(database.String, nullable=False)

    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
    
    def __repr__(self):
        return f"{self.name}: Category - {self.category}"