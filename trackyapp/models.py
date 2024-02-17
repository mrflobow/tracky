from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True,index=True)
    items = relationship("TrackItem", back_populates="project")


class TrackItem(Base):
    __tablename__ = "track_items"
    id = Column(Integer, primary_key=True)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    is_active = Column(Boolean, default=False)
    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="items")
