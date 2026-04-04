from pydantic import BaseModel, ConfigDict


class LessonSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    order_index: int


class CourseListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    description: str | None
    thumbnail_url: str | None
    order_index: int
    is_locked: bool


class CourseDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    description: str | None
    thumbnail_url: str | None
    order_index: int
    is_locked: bool
    lessons: list[LessonSummary]


class CourseCreate(BaseModel):
    title: str
    slug: str
    description: str | None = None
    thumbnail_url: str | None = None
    order_index: int = 0


class CourseUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    order_index: int | None = None
