from typing import Any, Optional
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
    course_id: int
    title: str
    slug: str
    order_index: int
    is_free: bool
    sections: list[LessonSectionOut] = []


class TaskCreate(BaseModel):
    task_type: str = "code_check"
    title: Optional[str] = None
    description: Optional[str] = None
    order_index: int = 0
    config: dict[str, Any] = {}

class SectionCreate(BaseModel):
    type: str
    title: Optional[str] = None
    order_index: int = 0
    content: Optional[dict[str, Any]] = None
    tasks: list[TaskCreate] = []

class LessonCreate(BaseModel):
    course_id: int
    title: str
    slug: str
    order_index: int = 1
    is_free: bool = False
    sections: list[SectionCreate] = []


class LessonUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    order_index: int | None = None
    is_free: bool | None = None
    sections: list[dict] | None = None