from enum import IntEnum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from application.security.schemas.user_schema import RolesFromUser


class LoginAuth(BaseModel):
    username: str = Field(min_length=3)
    password: str
     
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

class TokenData(BaseModel):
    user_id:str
    username: str
    email: str
    firstname: str
    lastname: str 
    roles: Optional[list[RolesFromUser]]

    
class EnumResultAuthenticate(IntEnum):
    AuthenticateSucessfull = 0,
    UserIsNone = 1,
    UserPasswordIncorrect = 2
