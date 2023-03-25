from sqlalchemy import Column, Identity, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.services.database.database import Base


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
