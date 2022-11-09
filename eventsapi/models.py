from typing import Annotated, Literal, Union
from pydantic import Field, BaseModel
from uuid import UUID


class DetailMessage(BaseModel):
    detail: str


class BaseEvent(BaseModel):
    course_id: int
    impression_id: UUID
    source_uri: str
    timestamp: int


class ContentLoadSuccessV1Event(BaseEvent):
    eventname: Literal['content_load_success_v1']
    content_id: UUID
    variant: str


class ContentLoadFailureV1Event(BaseEvent):
    eventname: Literal['content_load_failure_v1']
    content_id: UUID
    details: str


Event = Annotated[
    Union[
        ContentLoadSuccessV1Event,
        ContentLoadFailureV1Event
    ],
    Field(discriminator='eventname')
]
