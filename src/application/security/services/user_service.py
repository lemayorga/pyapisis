from contextlib import AbstractContextManager
from typing import Callable, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session 
from application.base_service import BaseSimpleService
from infra.database.models.security import User
from application.security.schemas.user_schema import UserDto, UserCreate
from application.auth.services.auth_service import *
from utils.context_auth_crypt import get_password_hash

class UserService(BaseSimpleService):

    def __init__(self, session_factory:  Callable[..., AbstractContextManager[Session]]) -> None:
        super(UserService, self).__init__(session_factory)

    
    def get_all(self) -> list[UserDto]:
        with self.session_factory() as session:
            objs: list[UserDto] = session.query(User).all()
            return objs
        

    def get_by_usernam(self, user_name: str) -> Optional[UserDto]:
        with self.session_factory() as session:
            objs: UserDto = session.query(User).filter(User.username == user_name).first()
            return objs
        
    def create(self, obj: UserCreate) -> UserDto:
        with self.session_factory() as session:
            user = session.query(User).filter(or_( User.email == obj.email.lower(), User.username == obj.username.lower())).first()
           
            if user is not None:
                raise Exception("User with this email already exist")

            user = User( 
                username = obj.username.lower(),
                email =  obj.email.lower(),
                password = get_password_hash(obj.password),
                firstname =  obj.firstname,
                lastname =  obj.lastname,
                is_active =  True
            )   

            session.add(user)
            session.commit()
            session.refresh(user)

            result_user: UserDto = user
            return result_user
    