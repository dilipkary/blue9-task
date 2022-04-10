import email
from re import U
from fastapi import APIRouter, Depends, Request
from auth.auth import get_current_user
from config.database import conn
from controllers.users import activate_user
from controllers.users import user_detail, user_login, user_signup
from models.user import users
from schemas.user import Pub_user, User
from datetime import datetime, timedelta
from typing import Optional
from fastapi import status
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

user = APIRouter(

)


'''@user.get("/")
async def selectall():
    return conn.execute(users.select()).fetchall()'''


@user.post("/signup", tags=["Signup"])
async def signup(user: User, request: Request):
    return user_signup(user, request)


@user.get("/activate/{confirmation_code}", tags=["Activation"])
async def activation(confirmation_code: str):
    return activate_user(confirmation_code)


@user.post("/login", status_code=status.HTTP_200_OK, tags=["login Authentication"])
async def login(request: OAuth2PasswordRequestForm = Depends()):
    return user_login(request)


@user.get("/{id}", tags=["User"])
async def get_user_detail(id: int, user: Pub_user = Depends(get_current_user)):
    return user_detail(id)


@user.get("/profile/", tags=["User"])
async def get_profile(user: Pub_user = Depends(get_current_user)):
    return user
