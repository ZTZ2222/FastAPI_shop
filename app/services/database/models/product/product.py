from sqlalchemy import Column, Identity, Integer, String, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

from app.services.database.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(String, unique=True, index=True)
    base_price = Column(Numeric(precision=8), server_default="1")
    sale_price = Column(Numeric(precision=8), server_default="1")
    description = Column(Text, default=None, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    category_id = Column(Integer, ForeignKey(
        'category.id', ondelete="CASCADE"), nullable=False)
    brand_id = Column(Integer, ForeignKey(
        'brand.id', ondelete="CASCADE"), nullable=True)

    category = relationship('Category', back_populates="products")
    brand = relationship('Brand', back_populates="products")
    comments = relationship('Comment', back_populates="product")
