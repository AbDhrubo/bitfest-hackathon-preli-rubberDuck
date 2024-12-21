from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Ingredient
from app.database import get_db
from pydantic import BaseModel

router = APIRouter()

# Pydantic model to validate the request body
class IngredientCreate(BaseModel):
    name: str
    quantity: float
    unit: str

@router.post("/")
def add_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    # Create a new Ingredient object using the validated data
    new_ingredient = Ingredient(
        name=ingredient.name,
        quantity=ingredient.quantity,
        unit=ingredient.unit
    )
    
    # Add the new ingredient to the database and commit the transaction
    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)
    
    return new_ingredient

@router.get("/")
def get_ingredients(db: Session = Depends(get_db)):
    return db.query(Ingredient).all()

@router.put("/{ingredient_id}")
def update_ingredient(ingredient_id: int, quantity: float, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    ingredient.quantity = quantity
    db.commit()
    return ingredient

@router.delete("/{ingredient_id}")
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    db.delete(ingredient)
    db.commit()
    return {"message": "Ingredient deleted"}
