
from typing import Optional
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel
from models.user import users
from config.database import conn
from config.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.JWTtoken import User, verify_token
from schemas.user import Pub_user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    return conn.execute(users.select().where(users.c.email == username)).fetchall()


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not verify_password(password, user[0]['password']):
        return False
    return True


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return {"id": token_data.id, "username": token_data.username, "usertype": token_data.usertype}


async def get_current_active_user(current_user: Pub_user = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
