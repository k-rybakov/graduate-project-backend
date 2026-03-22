from typing import Any
from pydantic import BaseModel, ConfigDict


class PracticeTaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_type: str
    title: str | None
    description: str | None
    order_index: int
    config: dict[str, Any]


class LessonSectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: str
    title: str | None
    order_index: int
    content: dict[str, Any] | None  # TipTap JSON; None for practice sections
    tasks: list[PracticeTaskOut]


class LessonOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    sections: list[LessonSectionOut]
