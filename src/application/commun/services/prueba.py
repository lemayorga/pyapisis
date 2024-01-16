from dependency_injector.wiring import inject, Provide
from src.infra.database.models.commun import Catalogue
from infra import Database, get_db
from fastapi import APIRouter, Depends, Path , status
from src.config.container import Dependencies
from sqlalchemy.orm import Session

@inject
def ejemplo(session1: Database = Depends(Provide[Dependencies.db]),  session2: Session = Depends(get_db)):
    # r1 = session1.query(Catalogue).all()
    r2 = session2.query(Catalogue).all()
    return 1