from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from . import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="True")
    is_superuser = Column(Boolean, server_default="False")
    address = Column(String)
    city = Column(String)
    country = Column(String)
    telephone = Column(String)

    orders = relationship('Order', back_populates="user")
    ratings = relationship('Rating', back_populates="user")
