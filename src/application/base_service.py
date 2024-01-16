
# https://patrick-muehlbauer.com/articles/fastapi-with-sqlalchemy

from contextlib import AbstractContextManager
from typing import Any, Callable, Generic, Optional, Type, TypeVar
import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from infra.database.setting_db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)

class BaseSimpleDBService:
    def __init__(self, session: Session) -> None:
        self._session = session

    @property
    def session(self) -> Session:
        return self._session
    
    
class BaseSimpleService:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

class BaseService(Generic[ModelType,GetSchemaType, CreateSchemaType, UpdateSchemaType]):
    
    def __init__(self, model: Type[ModelType],  session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.model = model
        self.session_factory = session_factory
 
    def get_by_id(self, id: Any) -> Optional[ModelType]:
        with self.session_factory() as session:
            obj: Optional[ModelType] = session.query(self.model).get(id)
            if obj is None:
                raise HTTPException(status_code=404, detail="Not Found")
            return obj

    def get_all(self) -> list[ModelType]:
        with self.session_factory() as session:
            objs: list[ModelType] = session.query(self.model).all()
            return objs
    
    def list_paginate(self, limit: int = 10, page: int = 1) -> list[ModelType]:
        with self.session_factory() as session:
            skip = (page - 1) * limit
            objs: list[ModelType] = session.query(self.model).slice(skip, skip + limit).all()
            return objs
        
    def create(self, obj: CreateSchemaType) -> ModelType:
        with self.session_factory() as session:
            db_obj: ModelType = self.model(**obj.dict())
            session.add(db_obj)
            try:
                session.commit()
            except sqlalchemy.exc.IntegrityError as e:
                session.rollback()
                if "duplicate key" in str(e):
                    raise HTTPException(status_code=409, detail="Conflict Error")
                else:
                    raise e
            return db_obj

    def update(self, id: Any, obj: UpdateSchemaType) -> Optional[ModelType]:
        with self.session_factory() as session:
            db_obj = session.query(self.model).get(id)
            for column, value in obj.dict(exclude_unset=True).items():
                setattr(db_obj, column, value)

            session.commit()
            return db_obj

    def delete(self, id: Any) -> bool:
        with self.session_factory() as session:
            db_obj = session.query(self.model).get(id)
            session.delete(db_obj)
            session.commit()
            return True