import logging
from asyncio import current_task
from typing import Callable
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, orm
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager, AbstractContextManager
from config.settings import get_settings

_SETTINGS = get_settings()

Base = declarative_base()
logger = logging.getLogger(__name__)

class Database:

    def __init__(self, db_url: str) -> None:
        self._engine = create_engine(db_url, echo=True)
        self._sessionmaker = sessionmaker(autocommit = False, autoflush = False, bind = self._engine)
        self._session_factory = orm.scoped_session(self._sessionmaker, scopefunc = current_task)

    @property
    def scoped_session(self):
        return self._session_factory
    

    def session_local(self):
        sessionLocal  = self._sessionmaker()
        return sessionLocal
    
    @property
    def get_db(self):
        sessionLocal  = self._sessionmaker()
        return sessionLocal
    
    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()

        logger.exception('Connecting to PostgreSQL')
        try:
            yield session
        except Exception:
            logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()

async def get_db() -> Session:
    logger.info("Connecting to PostgreSQL")
    database = Database(_SETTINGS.DATABASE_URL)
    db =  database.session_local()
    try:
        yield db  
        logger.info("Connection established")
    except Exception as ex:
        db.rollback()
        logger.exception(ex)
    finally:
        db .close()
        logger.info("Connection closed")