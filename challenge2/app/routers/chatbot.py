from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import requests
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models import Ingredient
from app.database import get_db

router = APIRouter()

class ChatbotRequest(BaseModel):
    query: str

@router.post("/suggest")
def recipe_chatbot(request: ChatbotRequest, db: Session = Depends(get_db)):
    user_input = request.query
    
    if not user_input:
        raise HTTPException(status_code=400, detail="No query provided")
    
    Ingredients = db.query(Ingredient).all()
    ingredient_names = [ingredient.name for ingredient in Ingredients]
    ingredients_list = ", ".join(ingredient_names)
    
    gemini_api_key = "AIzaSyAzcduRzH4OOcXF7AxMLiGWR6XeGLmK2xo"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_api_key}"
    
    user_input = f"{user_input}. Ingredients: {ingredients_list}"
    print(user_input)
    
    payload = {
        "contents": [{
            "parts": [{"text": user_input}]
        }]
    }
    
    # Set headers
    headers = {
        "Content-Type": "application/json"
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=payload)

    # Check for successful response
    if response.status_code == 200:
        try:
            response_data = response.json()  # Parse JSON response
            print("Gemini API Response:", response_data)  # Log the full response for debugging
            
            # Extract the recipe content from the response
            if "candidates" in response_data and len(response_data["candidates"]) > 0:
                recipe_response = response_data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Limit the response to 100 words
                recipe_words = recipe_response.split()
                limited_response = " ".join(recipe_words[:100]) + ("..." if len(recipe_words) > 100 else "")
                
                return JSONResponse(content={"response": limited_response}, status_code=200)
            else:
                raise HTTPException(status_code=500, detail="Error with Gemini API response: No candidates found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error parsing response: {str(e)}")
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Error {response.status_code}: {response.text}")
