import json
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from infra.database.setting_db import get_db
from utils.context_auth_crypt import verify_password, oauth2_scheme 
from config.settings import get_settings
from infra.database.models.security import User
from application.auth.schemas.auth_schema import EnumResultAuthenticate, LoginAuth, TokenData

# https://cosasdedevs.com/posts/autenticacion-login-jwt-fastapi/

_SETTINGS = get_settings()

async def authenticate_user(login: LoginAuth, session: Session) -> (EnumResultAuthenticate, User):
    user: User = session.query(User).filter(User.username == login.username.lower()).first()
    if not user:
        return (EnumResultAuthenticate.UserIsNone, None)
    
    if not verify_password(login.password, user.password):
        return (EnumResultAuthenticate.UserPasswordIncorrect, None) 
    
    return (EnumResultAuthenticate.AuthenticateSucessfull, user) 


def create_access_token(subject: User, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes = _SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
   
    token = TokenData( 
        user_id =  subject.id,
        username = subject.username,
        email = subject.email,
        firstname =  subject.firstname,
        lastname =  subject.lastname
    )
    to_encode = {
        "exp": expires_delta, 
        "data": str(json.dumps(token.__dict__)) 
    }
    encoded_jwt = jwt.encode(to_encode, _SETTINGS.JWT_SECRET_KEY, _SETTINGS.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: User, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes= _SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
       
    # roles =  subject.rols
    token = TokenData( 
        user_id =  subject.id,
        username = subject.username,
        email = subject.email,
        firstname =  subject.firstname,
        lastname =  subject.lastname,
        roles = [
            # RolesFromUser(user_id = subject.id, user_name= subject.username, rol_id= subject.rols.)
        ]
    )

    to_encode = {
        "exp": expires_delta, 
        "data": str(json.dumps(token.__dict__)) 
    }
    encoded_jwt = jwt.encode(to_encode, _SETTINGS.REFRESH_TOKEN_EXPIRE_MINUTES, _SETTINGS.ALGORITHM)
    return encoded_jwt

async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, 
    )
    try:
        payload = jwt.decode(token, _SETTINGS.JWT_SECRET_KEY, algorithms=[_SETTINGS.ALGORITHM])
        json_dict = json.loads(payload.get("data"))
        token_data = TokenData(**json_dict)
        if token_data is None:
            raise credentials_exception
        
        token_exp = payload.get("exp")
        if datetime.fromtimestamp(token_exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = db.query(User).filter(User.id == token_data.user_id).first()
        if user is None:
            raise credentials_exception
    
        return token_data
    except JWTError:
        raise credentials_exception


# https://stackoverflow.com/questions/73141350/override-global-dependency-for-certain-endpoints-in-fastapi