from fastapi import FastAPI
from app.routers import ingredients, recipes, chatbot
from app.database import Base, engine
from app.models import Ingredient

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mofa's Kitchen Buddy")

# Include routers
app.include_router(ingredients.router, prefix="/ingredients", tags=["Ingredients"])
app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Mofa's Kitchen Buddy API!"}