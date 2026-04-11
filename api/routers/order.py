from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import InternalError
from models import Order, OrderDetail
from schemas.order import OrderedOffers, OrderOfferRespone, OrderDetailsRespone

router = APIRouter(prefix="/orders", tags=["Orders and Order Details"])


@router.get("")
def get_orders(db: Session = Depends(get_db)):
    order = db.query(Order).all()
    return order


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    return order


@router.get("/{order_id}/order_details", response_model=list[OrderDetailsRespone])
def get_orders(
    order_id: int,
    db: Session = Depends(get_db)
):
    order_details = db.query(OrderDetail).filter(OrderDetail.order_id == order_id).all()
    return order_details


@router.post(
    "",
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
    buyer_id: int,
    ordered_offers: list[OrderedOffers],
    db: Session = Depends(get_db)
):
    try:
        order = Order(
            buyer_id = buyer_id
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
    
    except InternalError as e:
        db.rollback()
        error_message = str(e.orig).strip()

        raise HTTPException(
            status_code=404,
            detail=f"{error_message}"
        )


