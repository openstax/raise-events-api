import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from eventsapi import routers

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="RAISE Events API"
)

app.include_router(routers.v1_router, prefix="/v1")

CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS"
)

if CORS_ALLOWED_ORIGINS:
    # Support comma separated list of origins
    origins = [origin.strip() for origin in CORS_ALLOWED_ORIGINS.split(",")]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
