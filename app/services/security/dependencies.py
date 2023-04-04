from fastapi import Depends, HTTPException, status
from app.services.database.models.user import User
from app.services.security.oauth2 import get_current_user


async def admin_only(cur_user: User = Depends(get_current_user)):
    if not cur_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not enough permissions")

    return cur_user


# async def sub_required(cur_user: User = Depends(get_current_user)):
#     if not cur_user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                             detail="Must be logged in to access this resource")

#     return cur_user
