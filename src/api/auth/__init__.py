from fastapi import APIRouter
from api.auth.auth import router as router_auth

auth_router = APIRouter()
auth_router.include_router(
    router_auth
)