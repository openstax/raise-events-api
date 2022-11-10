from typing import Annotated, Literal, Union, Optional
from pydantic import Field, BaseModel
from uuid import UUID


class DetailMessage(BaseModel):
    detail: str


class BaseEvent(BaseModel):
    course_id: int
    impression_id: UUID
    source_uri: str
    timestamp: int


class ContentLoadedV1(BaseEvent):
    eventname: Literal['content_loaded_v1']
    content_id: UUID
    variant: str


class ContentLoadFailedV1(BaseEvent):
    eventname: Literal['content_load_failed_v1']
    content_id: UUID
    error: Optional[str] = ''


Event = Annotated[
    Union[
        ContentLoadedV1,
        ContentLoadFailedV1
    ],
    Field(discriminator='eventname')
]
