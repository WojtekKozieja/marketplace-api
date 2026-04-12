from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, InternalError
from psycopg2 import errors
from models import Order, OrderDetail, Offer
from schemas.order import OrderOffers, OrderOfferRespone, OrderDetailRespone, OrderResponse
from routers.auth import get_current_user
router = APIRouter(prefix="/users", tags=["Orders and Order Details"])


@router.get("/me/orders")
def get_orders(
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Page[OrderResponse]:
    order = db.query(Order).filter(Order.buyer_id == current_user_id)
    return paginate(db, order.order_by(Order.order_date.desc()))


@router.get("/me/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.order_id == order_id,
        Order.buyer_id == current_user_id
        ).first()
    return order


@router.get("/me/orders/{order_id}/order_details", response_model=list[OrderDetailRespone])
def get_order_details(
    order_id: int,
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order_details = db.query(OrderDetail).filter(
        Order.buyer_id == current_user_id,    
        OrderDetail.order_id == order_id
    ).all()
    return order_details


@router.post(
    "/me/orders",
    description=
    """
        You can order more than one offer.\n
        example input:\n
        [
            {
                "offer_id": 4,
                "quantity": 5
            },
            {
                "offer_id": 8,
                "quantity": 3
            }
        ]
    """,
    response_model=OrderOfferRespone)
def create_order(
    ordered_offers: list[OrderOffers],
    current_user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    offer_ids = [o.offer_id for o in ordered_offers]
    offer = db.query(Offer).filter(
        Offer.offer_id.in_(offer_ids),
        Offer.is_active == True,
        Offer.end_offer_date > func.now()
    ).all()

    if len(offer) != len(ordered_offers):
        raise HTTPException(status_code=404, detail="Offer not found")
    
    try:
        order = Order(
            buyer_id = current_user_id
        )
        db.add(order)
        db.flush()

        order_detail = []
        for temp_oq in ordered_offers:
            order_detail.append(OrderDetail(
                order_id = order.order_id,
                offer_id = temp_oq.offer_id,
                quantity = temp_oq.quantity,
                order_date = order.order_date
            ))

        db.add_all(order_detail)

        db.commit()
        db.refresh(order)
        return order
    
    except IntegrityError as e:
        db.rollback()
        
        if isinstance(e.orig, errors.ForeignKeyViolation):
            raise HTTPException(status_code=404, detail="Offer not found")
        elif isinstance(e.orig, errors.UniqueViolation):
            raise HTTPException(status_code=409, detail="Duplicate offer_id in order")
        raise HTTPException(status_code=500, detail="Database error")
     
    except InternalError as e:
        db.rollback()

        raise HTTPException(status_code=400,detail=str(e.orig).strip())

