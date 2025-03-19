from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import token
from .database import get_db
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(  db: Session = Depends(get_db),data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    token_payload= token.verify_token(data, credentials_exception)
    user = db.query(User).filter(User.email == token_payload.email).first()
    
    if user is None:
        raise credentials_exception

    return user