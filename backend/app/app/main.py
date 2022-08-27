from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.api_v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
DEBUG = True
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    if not DEBUG :
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else :
        app.add_middleware(
            CORSMiddleware,
            allow_origins='*',
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount(settings.STATICFILES_ENDPOINT, StaticFiles(directory= settings.UPLOAD_FILES_DIRS), name="static")