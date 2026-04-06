from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Category, Subcategory

router = APIRouter(prefix="/category", tags=["Categories and Subcategories"])

@router.get("/category")
def get_categories(db: Session = Depends(get_db)):
    results = db.query(Category).all()
    return results

@router.get("/Subcategory")
def get_subcategories(db: Session = Depends(get_db)):
    results = db.query(Subcategory).all()
    return results
