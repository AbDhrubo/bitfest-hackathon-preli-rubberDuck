# from fastapi import APIRouter, HTTPException, UploadFile
# from PIL import Image
# import pytesseract
# import io
# import os

# router = APIRouter()

# # Path to store recipes
# RECIPE_FILE_PATH = "my_fav_recipes.txt"

# # API to add a new recipe (either text or image)
# @router.post("/add_recipe/")
# async def add_recipe(recipe_text: str = None, file: UploadFile = None):
#     # If a recipe text is provided
#     if recipe_text:
#         try:
#             # Rename 'file' to 'recipe_file' to avoid conflict with the 'file' argument
#             with open(RECIPE_FILE_PATH, "a") as recipe_file:
#                 recipe_file.write(f"Recipe:\n{recipe_text}\n\n")
#             return {"message": "Recipe added successfully"}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to write text: {str(e)}")
    
#     # If an image file is provided, use OCR to extract text
#     if file:
#         try:
#             contents = await file.read()
#             image = Image.open(io.BytesIO(contents))
            
#             # Ensure pytesseract is installed and Tesseract is accessible
#             try:
#                 extracted_text = pytesseract.image_to_string(image)
#             except pytesseract.TesseractNotFoundError:
#                 raise HTTPException(status_code=500, detail="Tesseract OCR is not installed or not found.")
            
#             with open(RECIPE_FILE_PATH, "a") as recipe_file:
#                 recipe_file.write(f"Recipe (from image):\n{extracted_text}\n\n")
            
#             return {"message": "Recipe added from image successfully"}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

#     raise HTTPException(status_code=400, detail="Either recipe text or an image file must be provided")

# # API to retrieve all recipes
# @router.get("/get_recipes/")
# def get_recipes():
#     try:
#         with open(RECIPE_FILE_PATH, "r") as recipe_file:
#             recipes = recipe_file.read()
#         return {"recipes": recipes}
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="No recipes found")


from fastapi import APIRouter, HTTPException, Depends 
from sqlalchemy.orm import Session
from app.models import Recipe  # Relative import for the Recipe model
from app.database import get_db 
from app.database import SessionLocal
import os

router = APIRouter()

# Path to store recipes
RECIPE_FILE_PATH = "my_fav_recipes.txt"

from fastapi import APIRouter, HTTPException, Request
import os

router = APIRouter()

# Path to store recipes
RECIPE_FILE_PATH = "my_fav_recipes.txt"

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Recipe

router = APIRouter()

# Path to store recipes
RECIPE_FILE_PATH = "my_fav_recipes.txt"

@router.post("/add_recipe/")
async def add_recipe(request: Request):
    """
    Add a new recipe to the database and save the recipe text to a file.

    Parameters:
    - request: The request body containing recipe details.

    Returns:
    - Success message or HTTPException in case of an error.
    """
    try:
        body = await request.json()
        recipe_text = body.get("recipe_text")
        taste = body.get("taste", "Not specified")  # Default to "Not specified"
        cuisine_type = body.get("cuisine_type", "Not specified")
        preparation_time = body.get("preparation_time", None)
        reviews = body.get("reviews", None)

        if not recipe_text or not recipe_text.strip():
            raise HTTPException(status_code=400, detail="Recipe text cannot be empty")

        # Infer cuisine type and preparation time if not provided
        if cuisine_type == "Not specified":
            if "pasta" in recipe_text.lower() or "parmesan" in recipe_text.lower():
                cuisine_type = "Italian"
            elif "curry" in recipe_text.lower() or "spicy" in recipe_text.lower():
                cuisine_type = "Indian"
        
        if preparation_time is None:
            # Placeholder: Advanced models or manual input can improve this.
            preparation_time = len(recipe_text.split()) // 5  # Assume ~5 words per minute for a rough estimate.

        # Store the recipe in the database
        new_recipe = Recipe(
            title="Caesar Salad",  # Replace with actual parsing for title
            ingredients="[]",  # Replace with actual parsing for ingredients
            taste=taste,
            cuisine_type=cuisine_type,
            preparation_time=preparation_time,
            reviews=reviews or 0.0,
        )

        # Add the recipe to the database
        db: Session = SessionLocal()
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

        # Write the recipe text to the file
        try:
            with open(RECIPE_FILE_PATH, "a") as file:
                file.write(f"Recipe ID: {new_recipe.id}\n")
                file.write(f"Recipe Text: {recipe_text}\n\n")
        except Exception as file_error:
            raise HTTPException(status_code=500, detail=f"Failed to write recipe to file: {str(file_error)}")

        return {"message": "Recipe added successfully", "recipe_id": new_recipe.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add recipe: {str(e)}")





# API to retrieve all recipes
@router.get("/get_recipes/")
def get_recipes():
    """
    Retrieve all recipes from the recipe file.

    Returns:
    - A dictionary containing all recipes or an HTTPException if no recipes are found.
    """
    if not os.path.exists(RECIPE_FILE_PATH):
        raise HTTPException(status_code=404, detail="No recipes found")

    try:
        with open(RECIPE_FILE_PATH, "r") as file:
            recipes = file.read()
        return {"recipes": recipes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read recipes: {str(e)}")
