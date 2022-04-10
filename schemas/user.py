from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    password: str


class Pub_user(BaseModel):
    id: str
    username: str
    usertype: str


class JwtUser(BaseModel):
    username: str
    password: str
