from fastapi import APIRouter

from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.health_check import router as health_router

routers = APIRouter()
router_list = [user_router, health_router]

for router in router_list:
    routers.include_router(router)
