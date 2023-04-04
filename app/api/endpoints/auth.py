from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.services.database.schemas.security.token import Token
from app.services.database import DatabaseManager
from app.services.database.models.user import User
from app.utils.password_hashing import pwd_context
from app.services.security import oauth2


db = DatabaseManager()
db.initialize(settings)

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/login", response_model=Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(db.get_db_session)):
    async with session:
        user = await session.scalar(select(User).filter(User.email == user_credentials.username))

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")

    if not pwd_context.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid username or password")

    access_token = await oauth2.create_access_token(
        token_payload={
            "user_id": user.id,
            "sub": user.email
        }
    )

    return {"access_token": access_token, "token_type": "Bearer"}
