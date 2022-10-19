from src import database as db
from werkzeug.security import generate_password_hash, check_password_hash

class Category(db.Model):
    """
    Class that represents an ingredient category e.g Dairy
    This stores the following attributes
        category: (type: string)
    """
    #prevents default naming assumed from Class (model) name
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    ingredients = db.relationship('Ingredient',lazy='dynamic', back_populates="category",cascade='all, delete')

    def __init__(self, category: str):
        self.category = category
    
    def __repr__(self):
        return f"{self.category.title()}"

class Ingredient(db.Model):
    """
    Class that represents an ingredient
    This stores the following attributes
        name: (type: string)
        category: (type: string)
    """
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    category = db.relationship('Category',back_populates='ingredients', passive_deletes=True)
    recipe_ingredients = db.relationship("IngredientRecipe", lazy='dynamic', back_populates='ingredients', cascade='all, delete')

    def __init__(self, name: str, category_id: int):
        self.name = name
        # self.category = category
        self.category_id = category_id
    
    def __repr__(self):
        return f"{self.name.title()}"

class Recipe(db.Model):
    """
    Class that represents a recipe
    This stores the following attributes
        name: (type: string)
    """

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    steps = db.relationship('RecipeMethod',lazy=True, back_populates="recipe",cascade='all, delete')
    ingredients = db.relationship("IngredientRecipe",lazy=True, back_populates='recipe',cascade="all, delete")
    basket = db.relationship('BasketRecipes', lazy=True, back_populates="recipes", cascade="all, delete")

    def __init__(self, title: str):
        self.title = title
    
    def __repr__(self):
        return f"{self.title}"

class RecipeMethod(db.Model):
    """
    Class that represents new recipe model method
    This stores the following attributes:
        step: (type: string)
    """
    __tablename__ = 'recipemethods'

    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.String, nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)
    recipe = db.relationship('Recipe',back_populates='steps')

    def __init__(self, step: str, recipe_id: int):
        self.step = step
        self.recipe_id = recipe_id
    
    def __repr__(self):
        return f"{self.step}"

class IngredientRecipe(db.Model):
    """
    Class that represents the IngredienRecipe table. 
    Each row represents an ingredient linked to a recipe

    This stores the following attributes
        recipe_id: (type: int)
        ingredient_id: (type: int)
        Quantity: (type: Float)
        Unit: (type: string)
    """

    __tablename__ = 'ingredientrecipe'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)
    recipe = db.relationship("Recipe", back_populates="ingredients")
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete="CASCADE"), nullable=False)
    ingredients = db.relationship('Ingredient', back_populates='recipe_ingredients')
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)

    def __init__(self, recipe_id: int, ingredient_id: int, quantity: float, unit: str):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity
        self.unit = unit
    
    def __repr__(self):
        return f"Recipe: {self.recipe_id} Ingredient: {self.ingredient_id} Qty: {self.quantity}{self.unit}"

class Basket(db.Model):
    """
    Class to represent basket of recipes

    Stored the following attributes
        recipe: (str)
        quantityt: (int)
    """
    __tablename__ = 'basket'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    recipes = db.relationship('BasketRecipes', lazy=True, back_populates="basket", cascade="all, delete")

    def __init__(self, title):
        self.title = title

class BasketRecipes(db.Model):
    __tablename__ = 'basketrecipes'

    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('basket.id', ondelete='CASCADE'), nullable=False)
    basket = db.relationship('Basket', lazy=True, back_populates="recipes")
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete="CASCADE"), nullable=False)
    recipes = db.relationship('Recipe', lazy=True, back_populates="basket")
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, basket_id: int, recipe_id: int, quantity: int):
        self.basket_id = basket_id
        self.recipe_id = recipe_id
        self.quantity = quantity

class User(db.Model):
    """
    Class that represents a User

    This stores the following attributes
        name: (type: string)
        hashed_password: (type: string)
    """

    __tablename__ = 'users'

    #Specify schema
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    hashed_password = db.Column(db.String(128), nullable=False)

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