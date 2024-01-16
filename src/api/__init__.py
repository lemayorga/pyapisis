# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from infra.database.setting_db import  get_db
# from infra.database.seeds.init import execute_seed
# from api.commun import commun_router
# from api.security import security_router
# from api.auth import auth_router

# router = APIRouter()

# @router.get("/seeds", summary="Execute seeds")
# async def get(session: Session = Depends(get_db)): 
#    message = execute_seed(session)
#    return {"message": message } 


# router.include_router(auth_router)
# router.include_router(commun_router)
# router.include_router(security_router)


