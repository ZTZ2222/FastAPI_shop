from sqlalchemy import Boolean, Column, Identity, Integer, String, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.services.database.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(String, unique=True, index=True)
    base_price = Column(Numeric(precision=8), server_default="1")
    sale_price = Column(Numeric(precision=8), nullable=True)
    description = Column(Text, default=None, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    in_stock = Column(Boolean, nullable=False, default=True)
    category_id = Column(Integer, ForeignKey(
        'categories.id', ondelete="CASCADE"), nullable=False)
    brand_id = Column(Integer, ForeignKey(
        'brands.id', ondelete="CASCADE"), nullable=True)

    category = relationship('Category', back_populates="products")
    brand = relationship('Brand', back_populates="products")
    comments = relationship('Comment', back_populates="products")
