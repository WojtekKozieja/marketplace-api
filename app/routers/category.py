from database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Category, Subcategory

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
    return db.query(Category).filter(Category.category_id == category_id).first()


@router.get("/{category_id}/subcategories")
def get_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    return db.query(Subcategory).filter(Subcategory.category_id == category_id).all()


@router.get("/subcategories")
def get_subcategories(db: Session = Depends(get_db)):
    results = db.query(Subcategory).all()
    return results
