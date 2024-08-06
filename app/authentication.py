from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import ALGORITHM, SECRET_KEY
from app.crud import get_user_by_email
from app.main import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY: Optional[str] = SECRET_KEY


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if SECRET_KEY is None:
            raise ValueError("SECRET_KEY is not set")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user_by_email(db=db, email=email)  # Adjust this function as necessary
    if user is None:
        raise credentials_exception
    return user
