from pydantic import BaseConfig, BaseModel, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field (
        min_length=3,
        max_length=50,
        example="username"
    )
    email: EmailStr = Field(
        ...,
        example="myemail@dominio.com"
    )
    firstname: str = Field (
        min_length=3,
        max_length=100,
        example="firstname"
    )
    lastname: str = Field (
        min_length=3,
        max_length=100,
        example="lastname"
    )

    class Config(BaseConfig):
      validate_all = True
      orm_mode = True

class UserCreate(UserBase):
    password: str = Field(alias="password",
        min_length=8,
        max_length=64,
        example="strongpass"
    )
    
class UserUpdate(UserBase):
    ...

class UserDto(UserBase):
    id: int = Field(
        example="5"
    )
    is_active: bool 


class RolesFromUser(BaseModel):
    rol_id: int
    rol_name: str
    user_id: int
    user_name: str
