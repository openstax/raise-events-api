import os
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from eventsapi import routers
from auth import JWTBearer

logging.basicConfig(level=logging.INFO)

auth = JWTBearer()

app = FastAPI(
    title="RAISE Events API",
    dependencies=[Depends(auth)]
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
