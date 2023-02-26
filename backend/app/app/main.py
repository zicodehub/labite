from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import os
import sys

app_path = os.path.dirname(__file__)
app_path = os.path.dirname(app_path)
# app_path = os.path.dirname(app_path)
# app_path = os.path.abspath(app_path)
sys.path.insert(0, app_path)

print("My PATH  :: ", app_path, " ---  ", sys.path)

from app.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins

app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.mount(settings.STATICFILES_ENDPOINT, StaticFiles(directory= settings.UPLOAD_FILES_DIRS), name="static")
