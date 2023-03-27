import uuid
from sqlalchemy import UUID, Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.services.database.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4)
    full_name = Column(String, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default="True")
    is_superuser = Column(Boolean, server_default="False")

    comments = relationship('Comment', back_populates="user")
