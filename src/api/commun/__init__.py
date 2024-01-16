from fastapi import APIRouter, Depends
from application.auth.services.auth_service import get_current_user
from api.commun.catalogue import router as router_catalogue

commun_router = APIRouter(
    dependencies=[Depends(get_current_user)]
)
commun_router.include_router(router_catalogue)