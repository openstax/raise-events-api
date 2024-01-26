from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from eventsapi import routers
from eventsapi.auth import JWTBearer
from eventsapi.settings import AUTH_KEYS, CORS_ALLOWED_ORIGINS
from eventsapi.kafka_producer import aiokafka_producer

logging.basicConfig(level=logging.INFO)

auth_bearer = JWTBearer(AUTH_KEYS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await aiokafka_producer.start()
    yield
    await aiokafka_producer.stop()

app = FastAPI(
    title="RAISE Events API",
    dependencies=[Depends(auth_bearer)],
    lifespan=lifespan
)

app.include_router(routers.v1_router, prefix="/v1")

if CORS_ALLOWED_ORIGINS:
    # Support comma separated list of origins
    origins = [origin.strip() for origin in CORS_ALLOWED_ORIGINS.split(",")]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
