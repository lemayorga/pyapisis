from fastapi import APIRouter
from api.security.users import router as users_catalogue

security_router = APIRouter()
security_router.include_router(
    users_catalogue
)
