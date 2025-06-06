from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.errors.validation_error import request_validation_exception_handler
from app.core.db import get_mongo_client_manager
from app.core.logger import setup_logger
from ..api.ui.routes import api_router as ui_api_router
from ..api.host.routes import api_router as host_api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logger()
    db = get_mongo_client_manager()

    await db.start_async_mongo()
    yield
    await db.close_mongo()


app = FastAPI(title="ebShield", lifespan=lifespan)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.include_router(router=ui_api_router, prefix="/api")
app.include_router(router=host_api_router, prefix="/api")
app.add_api_route(
    "/openapi.json",
    include_in_schema=False,
    endpoint=lambda: app.openapi(),
)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
async def health():
    return "Health"
