import os
import logging
import json
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from eventsapi import routers
from eventsapi.auth import JWTBearer

logging.basicConfig(level=logging.INFO)

auth_keys = json.loads(os.environ['AUTH_KEYS'])
auth_bearer = JWTBearer(auth_keys)

app = FastAPI(
    title="RAISE Events API",
    dependencies=[Depends(auth_bearer)]
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
