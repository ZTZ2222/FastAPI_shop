from sqlalchemy import UUID, Column, Identity, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.services.database.session import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(Integer, ForeignKey(
        'products.id', ondelete='CASCADE'), nullable=False)

    user = relationship('User', back_populates="comments")
    product = relationship('Product', back_populates="comments")
