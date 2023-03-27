from sqlalchemy import Column, Identity, Integer, String
from sqlalchemy.orm import relationship

from app.services.database.session import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, Identity(always=True, cache=5), primary_key=True)
    name = Column(String, unique=True, index=True)

    products = relationship(
        'Product', back_populates="brand", cascade="all, delete", lazy=True)
