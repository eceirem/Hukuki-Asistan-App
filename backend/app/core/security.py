from __future__ import annotations

import hashlib
import hmac
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from app.core.config import settings

# HMAC-SHA256 pre-hashing encodes the password to a fixed 32-byte digest
# before passing it to bcrypt, bypassing bcrypt's 72-byte truncation limit.
_PEPPER = settings.SECRET_KEY.encode()


def _prehash(plain_password: str) -> bytes:
    digest = hmac.new(_PEPPER, plain_password.encode(), hashlib.sha256).digest()
    # bcrypt expects a base64-safe string; encode as hex (64 ASCII bytes, well under 72)
    return digest.hex().encode()


def hash_password(plain_password: str) -> str:
    hashed = bcrypt.hashpw(_prehash(plain_password), bcrypt.gensalt())
    return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_prehash(plain_password), hashed_password.encode())


def create_access_token(subject: str) -> str:
    """Return a signed JWT whose ``sub`` claim is *subject* (user UUID as str).

    Expiry is controlled by ``settings.ACCESS_TOKEN_EXPIRE_MINUTES``.
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
