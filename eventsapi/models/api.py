from typing import Annotated, Literal, Union, Optional
from pydantic import Field, BaseModel, AnyHttpUrl
from uuid import UUID


class DetailMessage(BaseModel):
    detail: str


class BaseEvent(BaseModel):
    course_id: int
    impression_id: UUID
    source_uri: AnyHttpUrl
    timestamp: int


class ContentLoadedV1(BaseEvent):
    eventname: Literal['content_loaded_v1']
    content_id: UUID
    variant: str


class ContentLoadFailedV1(BaseEvent):
    eventname: Literal['content_load_failed_v1']
    content_id: UUID
    error: Optional[str]


APIEvent = Annotated[
    Union[
        ContentLoadedV1,
        ContentLoadFailedV1
    ],
    Field(discriminator='eventname')
]
