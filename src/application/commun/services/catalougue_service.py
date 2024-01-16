from contextlib import AbstractContextManager
from typing import Callable
from sqlalchemy.orm import Session
from application.base_service import BaseService
from infra.database.models.commun import Catalogue
from application.commun.schemas.catalogue_schema import CatalogueBaseDto, CatalogueCreateDto, CatalogueUpdateDto

class CatalougueService(BaseService[CatalogueBaseDto, Catalogue, CatalogueCreateDto, CatalogueUpdateDto]):

    def __init__(self, session_factory:  Callable[..., AbstractContextManager[Session]]) -> None:
        super(CatalougueService, self).__init__(Catalogue, session_factory)


