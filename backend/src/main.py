from fastapi import APIRouter, FastAPI

from src.auth import router as auth_router
from src.users import router as users_router

app = FastAPI(
    docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json"
)
api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router.router)
api_router.include_router(users_router.router)

app.include_router(api_router)