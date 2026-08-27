import jwt
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

PBKDF2_ITERATIONS = 100_000

def hash_password(password: str) -> str:
    """Hash password using standard PBKDF2-HMAC-SHA256 with 100,000 iterations and random salt."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${salt}${dk.hex()}"

def verify_and_migrate_password(plain_password: str, hashed_password: str) -> Tuple[bool, bool]:
    """
    Verifies password against stored hash.
    Supports PBKDF2-HMAC-SHA256 and legacy SHA256 hashes.
    Returns (is_valid, needs_rehash).
    """
    if not hashed_password:
        return False, False

    if hashed_password.startswith("pbkdf2_sha256$"):
        try:
            parts = hashed_password.split("$", 2)
            if len(parts) == 3:
                _, salt, stored_hash = parts
                computed = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt.encode('utf-8'), PBKDF2_ITERATIONS).hex()
                return hmac.compare_digest(computed, stored_hash), False
        except Exception:
            return False, False

    # Legacy SHA256 fallback verification
    salted = f"{settings.SECRET_KEY}:{plain_password}".encode('utf-8')
    legacy_hash = hashlib.sha256(salted).hexdigest()
    if hmac.compare_digest(legacy_hash, hashed_password):
        return True, True  # Valid password, requires re-hashing to PBKDF2

    return False, False

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify hashed password."""
    valid, _ = verify_and_migrate_password(plain_password, hashed_password)
    return valid

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    now_utc = datetime.now(timezone.utc)
    if expires_delta:
        expire = now_utc + expires_delta
    else:
        expire = now_utc + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.models.models import User
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identity",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id = int(sub)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid user ID format in token")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_admin_user(current_user = Depends(get_current_user)):
    """Enforces ADMIN role requirement. Returns HTTP 403 Forbidden for non-admin users."""
    role = getattr(current_user, "role", "USER")
    if role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Admin diagnostics access required"
        )
    return current_user

