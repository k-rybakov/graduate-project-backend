from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProgressOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lesson_id: int
    completed_at: datetime


class CourseProgressOut(BaseModel):
    course_id: int
    completed_lesson_ids: list[int]
