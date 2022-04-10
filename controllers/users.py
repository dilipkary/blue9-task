
from asyncio.windows_events import NULL
from fastapi import HTTPException, Request, status
from auth.JWTtoken import create_access_token
from auth.auth import authenticate_user, get_password_hash, get_user
from config.database import conn
from controllers.sendmail import send_email_async
from schemas.user import JwtUser, User
from models.user import users
import uuid


def user_login(user: JwtUser):
    users = get_user(user.username)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    else:
        if not users[0]['is_active']:
            return {"message": "Activate Account"}
        if authenticate_user(user.username, user.password):
            data = {"sub": users[0]['email'], "id": users[0]
                    ['id'], "usertype": users[0]['type']}
            access_token = create_access_token(dict(data))

            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User or password is incorrect")


def user_signup(user: User, request):
    check = get_user(user.email)
    url = request.url._url
    confirmation_code = uuid.uuid4()
    if not check:
        conn.execute(users.insert().values(
            name=user.name,
            email=user.email,
            password=get_password_hash(user.password),
            confirmation=confirmation_code
        ))
        domain = url.split("signup")[0]
        # rs = {"activation_url": domain+"activate/" +
        #   str(confirmation_code), "message": "Success"}
        send_email_async("Account Activation", user.email,
                         "your activation link is "+domain+"activate/"+str(confirmation_code))
        return {"message": "activation mail sent"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User already exist with this email ID")


def activate_user(confirmation_code):
    user = conn.execute(users.select().where(
        users.c.confirmation == confirmation_code)).fetchall()
    if user[0]['is_active'] == True:
        return {"message": "Account Already Activated"}
    if user:
        check = conn.execute(users.update().values(
            is_active=True
        ).where(
            users.c.confirmation == confirmation_code))
        if check:
            return {"message": "Account Activation Successfull"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not available")


def user_detail(id):
    user = conn.execute(users.select().where(users.c.id == id)).fetchall()
    data = {"id": user[0]['id'], "name": user[0]
            ['name'], "email": user[0]['email']}
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} is not available")
    else:
        return data


def get_profile(id):
    user = conn.execute(users.select().where(users.c.id == id)).fetchall()
    data: User = user[0]
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} is not available")
    else:
        return data
