from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import Recipe, Ingredient
from app.database import get_db
from typing import List

router = APIRouter()

@router.get("/suggest")
def suggest_recipe(preference: str, db: Session = Depends(get_db)):
    available_ingredients = db.query(Ingredient).all()
    recipes = db.query(Recipe).filter(Recipe.taste == preference).all()

    suitable_recipes = []
    for recipe in recipes:
        recipe_ingredients = json.loads(recipe.ingredients)
        if all(
            any(ing.name == r_ing for ing in available_ingredients)
            for r_ing in recipe_ingredients
        ):
            suitable_recipes.append(recipe)
    
    return suitable_recipes
