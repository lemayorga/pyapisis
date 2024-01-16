from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from application.auth.services.auth_service import get_current_user
from infra.database.setting_db import get_db
from infra.database.seeds.init import execute_seed
from application.auth.schemas.auth_schema import TokenData
from api.commun import commun_router
from api.security import security_router
from api.auth import auth_router

router = APIRouter()

@router.get('/')
def home():
    return {"message": "Hello World"}


@router.get("/seeds", summary="Execute seeds")
async def get(session: Session = Depends(get_db), user: TokenData = Depends(get_current_user)): 
   message = execute_seed(session)
   return {"message": message } 


router.include_router(auth_router)
router.include_router(commun_router)
router.include_router(security_router)


