from typing import Annotated, Literal, Union, Optional
from pydantic import Field, BaseModel
from uuid import UUID


CONTENT_LOADED_V1 = 'content_loaded_v1'
CONTENT_LOAD_FAILED_V1 = 'content_load_failed_v1'


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
    error: Optional[str]


Event = Annotated[
    Union[
        ContentLoadedV1,
        ContentLoadFailedV1
    ],
    Field(discriminator='eventname')
]


class BaseKafkaEventV1(BaseModel):
    user_uuid: UUID
    course_id: int
    impression_id: UUID
    source_scheme: str
    source_host: str
    source_path: str
    source_query: str
    timestamp: int


class KafkaContentLoadedV1(BaseKafkaEventV1):
    content_id: UUID
    variant: str


class KafkaContentLoadFailedV1(BaseKafkaEventV1):
    content_id: UUID
    error: Optional[str]
