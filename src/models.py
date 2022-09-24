from src import database
from werkzeug.security import generate_password_hash, check_password_hash

class Category(database.Model):
    """
    Class that represents an ingredient category e.g Dairy

    This stores the following attributes
        category: (type: string)
    """
    #prevents default naming assumed from Class (model) name
    
    __tablename__ = 'categories'

    id = database.Column(database.Integer, primary_key=True)
    category = database.Column(database.String, nullable=False)
    #Provide the one to many link between Category and Ingredient
    ingredients = database.relationship('Ingredient', backref='category', lazy='dynamic')

    def __init__(self, category: str):
        self.category = category
    
    def __repr__(self):
        return f"Category - {self.category}"

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
    # category = database.Column(database.String, nullable=False)
    category_id = database.Column(database.Integer, database.ForeignKey('categories.id'))

    def __init__(self, name: str, category_id: int):
        self.name = name
        # self.category = category
        self.category_id = category_id
    
    def __repr__(self):
        return f"{self.name}"
        # return f"{self.name}: Category - {self.category}"

class User(database.Model):
    """
    Class that represents a User

    This stores the following attributes
        name: (type: string)
        hashed_password: (type: string)
    """

    __tablename__ = 'users'

    #Specify schema
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    hashed_password = database.Column(database.String(128), nullable=False)

    def __init__(self, name: str, email: str, password_plaintext: str):
        self.name = name
        self.email = email
        self.hashed_password = self.hash_password(password_plaintext)
    
    def is_password_correct(self, test_password: str) -> bool:
        return check_password_hash(self.hashed_password, self.hash_password(test_password))

    @staticmethod
    def hash_password(password_plaintext: str) -> str:
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f"{self.name}: Email: {self.email}"