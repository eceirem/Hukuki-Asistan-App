from __future__ import annotations

import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.crud_user import get_user_by_id
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import TokenPayload

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: Annotated[str, Depends(_oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    try:
        raw = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        payload = TokenPayload(**raw)
    except (JWTError, Exception):
        raise _CREDENTIALS_EXCEPTION

    if payload.sub is None:
        raise _CREDENTIALS_EXCEPTION

    try:
        user_id = uuid.UUID(payload.sub)
    except ValueError:
        raise _CREDENTIALS_EXCEPTION

    user = await get_user_by_id(db, user_id)

    if user is None:
        raise _CREDENTIALS_EXCEPTION

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account.",
        )

    return user


# Convenience type alias — used in route signatures.
CurrentUser = Annotated[User, Depends(get_current_user)]
