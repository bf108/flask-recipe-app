from src.models import Ingredient, Category
from src import database as db
import json

with open('src/static/category_groups.json','r') as f:
    var = json.load(f)

for k, val in var.items():
    new_k = " ".join(k.split('_')) if '_' in k else k
    try:
        db.session.add(Category(new_k))
    except:
        print(new_k)
db.session.commit()
    
for k, val in var.items():
    new_k = " ".join(k.split('_')) if '_' in k else k
    try:
        db.session.add(Category(new_k))
    except:
        print(new_k)
db.session.commit()

ingredients_ = []
ing_check = []
for k, cat_ingredients in var.items():
    new_k = " ".join(k.split('_')) if '_' in k else k
    cat_id = Category.query.filter_by(category=new_k).first().id
    for i in cat_ingredients:
        if i not in ing_check:
            ing_check.append(i)
            ingredients_.append(Ingredient(name=i, category_id=cat_id, category_name=new_k))
for c in ingredients_:
    db.session.add(c)
db.session.commit()

db.session.rollback()