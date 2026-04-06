
from sqlalchemy import ForeignKey, ForeignKeyConstraint, Column, Table, BigInteger, Integer, DateTime, String, VARCHAR, SmallInteger, func, text, Numeric, Boolean, CHAR
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)

    first_name = Column(VARCHAR(30), nullable=False)
    second_name = Column(VARCHAR(30), nullable=False)
    email = Column(VARCHAR(50), unique=True, nullable=False)
    password = Column(CHAR(60), nullable=False)

    offers = relationship("Offer", back_populates="seller")
    #historical_offers = relationship("HistoricalOffer", back_populates="user")
    orders = relationship("Order", back_populates="buyer")
    fav_offers = relationship(
        "Offer",
        secondary="favourites",
        primaryjoin="User.user_id == favourites.c.user_id",
        secondaryjoin="Offer.offer_id == favourites.c.offer_id",
        back_populates="favourites_by"
    )


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(SmallInteger, primary_key=True)
    category_name = Column(VARCHAR(20), unique= True, nullable=False)

class Subcategory(Base):
    __tablename__ = "subcategories"

    subcategory_id = Column(SmallInteger, primary_key=True)
    subcategory_name = Column(VARCHAR(20), nullable=False)

    category_id = Column(SmallInteger, ForeignKey("categories.category_id"))

    offers = relationship("Offer", back_populates="subcategory")


class Offer(Base):
    __tablename__ = "offers"

    offer_id = Column(BigInteger, primary_key=True)

    seller_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    subcategory_id = Column(SmallInteger, ForeignKey("subcategories.subcategory_id"), nullable=False)
    unit_price = Column(Numeric(10,2), nullable=False)
    quantity = Column(Integer, nullable=False)
    title = Column(VARCHAR(50), nullable=False)
    description = Column(VARCHAR(1000), nullable=False)
    photo = Column(VARCHAR(100), nullable = False)
    start_offer_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    end_offer_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP + INTERVAL '30 days'"))
    is_active = Column(Boolean, server_default="TRUE")
    

    seller = relationship("User", foreign_keys=[seller_id], back_populates="offers")
    orderdetails = relationship("OrderDetail", back_populates="offer")
    subcategory = relationship("Subcategory", back_populates="offers")
    favourites_by = relationship(
        "User", 
        secondary="favourites",
        primaryjoin="Offer.offer_id == favourites.c.offer_id",
        secondaryjoin="User.user_id == favourites.c.user_id",
        back_populates="fav_offers",
    )


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(BigInteger, primary_key=True)

    buyer_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    order_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    buyer = relationship("User", back_populates="orders")
    orderdetails = relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "order_details"

    order_id = Column(BigInteger, primary_key=True)
    offer_id = Column(BigInteger, primary_key=True)
    order_date = Column(DateTime, primary_key=True)

    unit_price = Column(Numeric(10,2))
    quantity = Column(Integer)
    title = Column(String(50))
    photo = Column(VARCHAR(100))
    is_active = Column(Boolean)

    __table_args__ = (
        ForeignKeyConstraint(
            ["offer_id", "is_active"],
            ["offers.offer_id", "offers.is_active"]
        ),
        ForeignKeyConstraint(
            ["order_id", "order_date"],
            ["orders.order_id", "orders.order_date"]
        )
    )

    offer = relationship("Offer", back_populates="orderdetails")
    order = relationship("Order", back_populates="orderdetails")


class PriceLogs(Base):
    __tablename__ = "price_logs"

    offer_id = Column(BigInteger, primary_key=True)
    changed_date = Column(DateTime, primary_key=True, server_default=text("CURRENT_TIMESTAMP"))
    new_price = Column(Numeric(10,2), nullable=False)
    is_active = Column(Boolean, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["offer_id", "is_active"],
            ["offers.offer_id", "offers.is_active"]
        ),
    )
    

favourites = Table(
    "favourites",
    Base.metadata,
    Column("user_id", BigInteger, ForeignKey("users.user_id"), primary_key=True),
    Column("offer_id", BigInteger, primary_key=True),
    Column("is_active", Boolean, primary_key=True, server_default=text("TRUE")),
    ForeignKeyConstraint(
        ["offer_id", "is_active"],
        ["offers.offer_id", "offers.is_active"]
    ),
)


