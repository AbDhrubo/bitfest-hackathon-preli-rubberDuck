from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


from sqlalchemy import Column, Integer, String, Float
from app.database import Base  # Assuming you have a Base class for your SQLAlchemy models

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float)
    unit = Column(String)  



class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(Text)  # JSON string storing ingredient IDs and quantities
    taste = Column(String)
    cuisine_type = Column(String)
    preparation_time = Column(Integer)
    reviews = Column(Float)
