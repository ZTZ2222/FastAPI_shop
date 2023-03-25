from sqlalchemy import Column, Identity, Integer, String, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="True")
    is_superuser = Column(Boolean, server_default="False")

    comments = relationship('Comment', back_populates="user")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(String, unique=True, index=True)
    category_id = Column(Integer, ForeignKey(
        'category.id', ondelete="CASCADE"), nullable=False)
    brand_id = Column(Integer, ForeignKey(
        'brand.id', ondelete="CASCADE"), nullable=True)
    price = Column(Numeric(precision=8), server_default="1")
    description = Column(Text, default=None, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

    category = relationship('Category', back_populates="products")
    brand = relationship('Brand', back_populates="products")
    comments = relationship('Comment', back_populates="product")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey(
        'product.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates="comments")
    product = relationship('Product', back_populates="comments")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(String, unique=True, index=True)

    products = relationship('Product', back_populates="category", lazy=True)


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(String, unique=True, index=True)

    products = relationship(
        'Product', back_populates="brand", cascade="all, delete", lazy=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True, nullable=False)
    address = Column(String, index=True)
    city = Column(String, index=True)
    country = Column(String, index=True)
    telephone = Column(String, index=True)

    items = relationship('Item', back_populates="order")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(String, unique=True, index=True)
    order_id = Column(Integer, ForeignKey(
        'order.id', ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey(
        'product.id', ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(precision=8), server_default="1")
    quantity = Column(Integer)

    order = relationship('Order', back_populates="items")
