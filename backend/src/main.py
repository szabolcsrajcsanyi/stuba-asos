from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from fastapi import APIRouter, FastAPI
from dotenv import load_dotenv

from src.auth import router as auth_router
from src.users import router as users_router
from src.status import router as status_router
from src.tickets import router as ticket_router


load_dotenv()


origins = ["*"]
middleware = [
    Middleware(
        CORSMiddleware, 
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]
app = FastAPI(
    middleware=middleware,
    docs_url="/api/docs",
    redoc_url="/api/redoc", 
    openapi_url="/api/openapi.json"
)

api_router = APIRouter(prefix="/api")
api_router.include_router(status_router.router)
api_router.include_router(auth_router.router)
api_router.include_router(users_router.router)
api_router.include_router(ticket_router.router)
app.include_router(api_router)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )