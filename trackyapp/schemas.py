from datetime import datetime

from pydantic import BaseModel


class TrackItemBase(BaseModel):
    pass

class TrackItemCreate(TrackItemBase):
    startTime: datetime

class TrackItemStop(TrackItemBase):
    endTime: datetime

class TrackItem(TrackItemBase):
    id: int
    project_id: int
    is_active: bool
    startTime: datetime | None
    endTime: datetime | None

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    items: list[TrackItem] = []

    class Config:
        from_attributes = True



