from dependency_injector import containers, providers
from infra.database.setting_db import Database
from application.base_service import BaseService,BaseSimpleService
from config.settings import get_settings
from application.commun.services.catalougue_service import CatalougueService
from application.security.services.user_service import   UserService


_SETTINGS = get_settings()

class Dependencies(containers.DeclarativeContainer):
   config = providers.Configuration()

   wiring_config = containers.WiringConfiguration(
      packages=[
         "application.base_service",
         "api.commun",
         "api.security",
         "api.auth",
      ]
   )

   # db = providers.Singleton(Database, db_url = _SETTINGS.DATABASE_URL)
   db = providers.Factory(Database, db_url = _SETTINGS.DATABASE_URL)
   base_simple_service = providers.Factory(BaseSimpleService, session_factory = db.provided.session)   
   base_service = providers.Factory(BaseService, session_factory = db.provided.session)
   catalougue_service = providers.Factory(CatalougueService, session_factory = db.provided.session)
   user_service = providers.Factory(UserService, session_factory = db.provided.session)

