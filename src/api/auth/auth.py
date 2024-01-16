from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException , status
from fastapi.security import OAuth2PasswordRequestForm
from infra.database.setting_db import  get_db
from application.auth.services.auth_service import authenticate_user, create_access_token, create_refresh_token, get_current_user
from application.auth.schemas.auth_schema import EnumResultAuthenticate, LoginAuth, TokenData, TokenSchema


router = APIRouter(
     prefix='/api/auth',
     tags=['Auth']
)
table_name = router.tags[0]


@router.post('/loginOAuth', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def loginOAuth(form_data: OAuth2PasswordRequestForm = Depends(),  session: Session = Depends(get_db)):
    login = LoginAuth(username = form_data.username, password = form_data.password)
    (result, user) = await authenticate_user(login,session)
    if result ==  EnumResultAuthenticate.UserIsNone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User incorrect"
        )

    if result ==  EnumResultAuthenticate.UserPasswordIncorrect:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect user or password"
        )
    
    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(login: LoginAuth = Body(),  session: Session = Depends(get_db)):
    (result, user) = await authenticate_user(login,session)

    if result ==  EnumResultAuthenticate.UserIsNone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User incorrect"
        )

    if result ==  EnumResultAuthenticate.UserPasswordIncorrect:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect user or password"
        )
    
    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user),
    }

 
@router.get('/me', summary='Get details of currently logged in user', response_model=TokenData)
async def get_me(user: TokenData = Depends(get_current_user)):
    return user

# https://www.freecodecamp.org/news/how-to-add-jwt-authentication-in-fastapi/