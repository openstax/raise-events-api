import logging
from typing import List
from fastapi import APIRouter, Depends
from eventsapi import auth
from eventsapi.models import Event, DetailMessage

logger = logging.getLogger(__name__)

v1_router = APIRouter()


@v1_router.post(
    "/events",
    status_code=201,
    response_model=DetailMessage)
async def create_events(
    events: List[Event],
    user_uuid: str = Depends(auth.get_user_uuid)
):
    logger.info("Received POST to /events")
    return {"detail": "Success!"}
