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

class Recipe(database.Model):
    """
    Class that represents a recipe

    This stores the following attributes
        name: (type: string)
        method: (type: Text)
    """

    __tablename__ = 'recipes'

    id = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String, nullable=False, unique=True)
    method = database.Column(database.Text, nullable=False, default='Just make it!')
    #One to Many relationship between recipe and rows in the IngredientRecipe Table
    # ingredient_recipe = database.relationship('IngredientRecipe', backref='recipe', lazy='dynamic')

    def __init__(self, title: str, method: str):
        self.title = title
        self.method = method
    
    def __repr__(self):
        return f"{self.title}"

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
    email = database.Column(database.String, nullable=False, unique=True)
    hashed_password = database.Column(database.String(128), nullable=False)

    def __init__(self, email: str, password_plaintext: str):
        self.email = email
        self.hashed_password = self.hash_password(password_plaintext)
    
    def is_password_correct(self, test_password: str) -> bool:
        return check_password_hash(self.hashed_password, test_password)

    @staticmethod
    def hash_password(password_plaintext: str) -> str:
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f"Email: {self.email}"
    
    @property
    def is_authenticated(self):
        """Return True if the user has been successfully registered."""
        return True

    @property
    def is_active(self):
        """Always True, as all users are active."""
        return True

    @property
    def is_anonymous(self):
        """Always False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the user ID as a unicode string (`str`)."""
        return str(self.id)