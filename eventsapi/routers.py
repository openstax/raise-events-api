import logging
from fastapi import APIRouter
from eventsapi import models

logger = logging.getLogger(__name__)

v1_router = APIRouter()


@v1_router.post(
    "/events",
    status_code=201,
    response_model=models.DetailMessage)
def create_events():
    logger.info("Received POST to /events")
    return {"detail": "Success!"}
