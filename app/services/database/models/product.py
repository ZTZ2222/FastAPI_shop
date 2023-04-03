from sqlalchemy import Boolean, CheckConstraint, Column, Float, Integer, String, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship

from . import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    name = Column(String, index=True)
    base_price = Column(Numeric(precision=8), server_default="1")
    sale_price = Column(Numeric(precision=8), nullable=True)
    description = Column(Text, nullable=True)
    in_stock = Column(Boolean, nullable=False, default=True)
    category_id = Column(Integer, ForeignKey(
        'categories.id', ondelete="CASCADE"), nullable=False)
    brand_id = Column(Integer, ForeignKey(
        'brands.id', ondelete="CASCADE"), nullable=True)
    color_id = Column(Integer, ForeignKey(
        'colors.id', ondelete="CASCADE"), nullable=True)
    size_id = Column(Integer, ForeignKey(
        'sizes.id', ondelete="CASCADE"), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)

    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    color = relationship("Color", back_populates="products")
    size = relationship("Size", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    ratings = relationship("Rating", back_populates="product")


class Color(BaseModel):
    __tablename__ = 'colors'

    name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="color")


class Size(BaseModel):
    __tablename__ = 'sizes'

    name = Column(String, unique=True, index=True)

    products = relationship("Product", back_populates="size")


class Rating(BaseModel):
    __tablename__ = "ratings"

    user_id = Column(Integer, ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey(
        'products.id', ondelete='CASCADE'), nullable=False)
    stars = Column(Float, CheckConstraint(
        'stars>=0 and stars<=5'), nullable=False)
    comment = Column(String(250), nullable=True)

    user = relationship('User', back_populates="ratings")
    product = relationship('Product', back_populates="ratings")
