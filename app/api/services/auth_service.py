from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

fake_users_db: Dict[str, Dict[str, str]] = {
    "user@example.com": {"email": "user@example.com", "password": "hashedpassword"}
}


def authenticate_user(email: str, password: str) -> Optional[Dict[str, str]]:
    user: Optional[Dict[str, str]] = fake_users_db.get(email)
    if not user or user["password"] != password:
        return None
    return user


def create_access_token(data: dict) -> str:
    expire: datetime = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode: Dict[str, Any] = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
