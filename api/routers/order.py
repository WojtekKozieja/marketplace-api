from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import InternalError
from models import Order, OrderDetail
from schemas.order import OrderedOffers, OrderOfferRespone

router = APIRouter(prefix="/order", tags=["Order and Order Details"])


@router.get("/orders")
def get_offers(db: Session = Depends(get_db)):
    order = db.query(Order).all()
    return order


@router.get("/order_details")
def get_orders(db: Session = Depends(get_db)):
    orderdetails = db.query(OrderDetail).all()
    return orderdetails


@router.get("{order_id}/order_and_order_details/")
def get_orders_and_order_details( order_id: int, db: Session = Depends(get_db)):
    result = db.query(Order, OrderDetail).join(OrderDetail).filter(Order.order_id == order_id).all()
    return [
        {**order.__dict__, **orderdetails.__dict__}
        for order, orderdetails in result
    ]


@router.post(
    "/take_an_order/{buyer_id}",
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


@router.get("/get_users_orders_by_id/{user_id}", response_model=OrderOfferRespone)
def get_users_orders_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):
    result = db.query(Order).filter(Order.buyer_id == user_id).first()
    return result
