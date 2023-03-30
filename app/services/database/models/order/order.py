from sqlalchemy import Column, Integer, String, Numeric, Identity, ForeignKey
from sqlalchemy.orm import relationship

from app.services.database.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    full_name = Column(String)
    email = Column(String, index=True, nullable=False)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    telephone = Column(String)

    items = relationship('Item', back_populates="order")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(String, unique=True)
    order_id = Column(Integer, ForeignKey(
        'orders.id', ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey(
        'products.id', ondelete="CASCADE"), nullable=False)
    base_price = Column(Numeric(precision=8), server_default="1")
    sale_price = Column(Numeric(precision=8), server_default="1")
    quantity = Column(Integer)

    order = relationship('Order', back_populates="items")
