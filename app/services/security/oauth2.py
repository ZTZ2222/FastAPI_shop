from datetime import datetime, timedelta
from typing import Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.services.database.schemas.security.token import TokenPayload
from app.services.database import DatabaseManager
from app.services.database.models.user import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="api/v1/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

db = DatabaseManager()
db.initialize(settings)


async def create_access_token(token_payload: dict[str: Any]) -> str:
    to_encode = token_payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def verify_access_token(token: str, credential_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        sub = payload.get("sub")

        if id is None:
            raise credential_exception

        token_data = TokenPayload(user_id=user_id, sub=sub)

    except JWTError:
        raise credential_exception

    return token_data


async def get_current_user(token: str = Depends(reusable_oauth2), session: AsyncSession = Depends(db.get_db_session)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token_verified = await verify_access_token(token, credentials_exception)

    async with session:
        user = await session.scalar(select(User).filter(User.email == token_verified.sub))

    return user
