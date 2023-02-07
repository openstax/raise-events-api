from typing import Annotated, List, Literal, Union, Optional
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


class IbPsetProblemAttemptedV1(BaseEvent):
    eventname: Literal['ib_pset_problem_attempted_v1']
    content_id: UUID
    variant: str
    problem_type: str
    response: Union[str, List[str]]
    correct: bool
    attempt: int
    final_attempt: bool
    pset_content_id: UUID
    pset_problem_content_id: UUID


APIEvent = Annotated[
    Union[
        ContentLoadedV1,
        ContentLoadFailedV1,
        IbPsetProblemAttemptedV1
    ],
    Field(discriminator='eventname')
]
