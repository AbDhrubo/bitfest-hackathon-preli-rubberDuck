from fastapi import APIRouter, HTTPException, UploadFile
from PIL import Image
import pytesseract
import io
import os

router = APIRouter()

# Path to store recipes
RECIPE_FILE_PATH = "my_fav_recipes.txt"

# API to add a new recipe (either text or image)
@router.post("/add_recipe/")
async def add_recipe(recipe_text: str = None, file: UploadFile = None):
    # If a recipe text is provided
    if recipe_text:
        try:
            # Rename 'file' to 'recipe_file' to avoid conflict with the 'file' argument
            with open(RECIPE_FILE_PATH, "a") as recipe_file:
                recipe_file.write(f"Recipe:\n{recipe_text}\n\n")
            return {"message": "Recipe added successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to write text: {str(e)}")
    
    # If an image file is provided, use OCR to extract text
    if file:
        try:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            # Ensure pytesseract is installed and Tesseract is accessible
            try:
                extracted_text = pytesseract.image_to_string(image)
            except pytesseract.TesseractNotFoundError:
                raise HTTPException(status_code=500, detail="Tesseract OCR is not installed or not found.")
            
            with open(RECIPE_FILE_PATH, "a") as recipe_file:
                recipe_file.write(f"Recipe (from image):\n{extracted_text}\n\n")
            
            return {"message": "Recipe added from image successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

    raise HTTPException(status_code=400, detail="Either recipe text or an image file must be provided")

# API to retrieve all recipes
@router.get("/get_recipes/")
def get_recipes():
    try:
        with open(RECIPE_FILE_PATH, "r") as recipe_file:
            recipes = recipe_file.read()
        return {"recipes": recipes}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="No recipes found")
