from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from sqlalchemy.orm import Session
from models import Category, Subcategory
from schemas.category import SubcategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories and Subcategories"])

@router.get("")
def get_categories(db: Session = Depends(get_db)):
    results = db.query(Category).all()
    return results


@router.get("/{category_id}")
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    result = db.query(Category).filter(Category.category_id == category_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return result


@router.get("/{category_id}/subcategories", response_model=list[SubcategoryResponse])
def get_subcategories(
    category_id: int,
    db: Session = Depends(get_db)
):
    result = db.query(Subcategory).filter(Subcategory.category_id == category_id).all()
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    return result