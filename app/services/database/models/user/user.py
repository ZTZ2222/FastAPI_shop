import uuid
from sqlalchemy import UUID, Column, String, Boolean
from sqlalchemy.orm import relationship

from app.services.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    username = Column(String, nullable=False, index=True)
    full_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="True")
    is_superuser = Column(Boolean, server_default="False")

    ratings = relationship('Rating', back_populates="user")
