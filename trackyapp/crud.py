import datetime

from sqlalchemy.orm import Session

from . import models, schemas


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_project_by_name(db: Session, name: str):
    return db.query(models.Project).filter(models.Project.name == name).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(name=project.name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TrackItem).offset(skip).limit(limit).all()


def get_items_by_project(db: Session, project_id: int):
    return db.query(models.TrackItem).filter(models.TrackItem.project_id == project_id).all()


def get_active_item_by_project(db: Session, project_id: int):
    return db.query(models.TrackItem).filter(models.TrackItem.project_id == project_id).filter(
        models.TrackItem.is_active == True).first()


def stop_item(db: Session, item: schemas.TrackItemStop, item_id: int):
    db_item = db.query(models.TrackItem).filter(models.TrackItem.id == item_id).first()

    db_item.endTime = item.endTime
    db_item.is_active = False
    db.commit()
    db.refresh(db_item)
    return db_item


def create_project_item(db: Session, item: schemas.TrackItemCreate, project_id: int):
    db_item = models.TrackItem(**item.model_dump(), project_id=project_id)
    db_item.startTime = item.startTime
    db_item.is_active = True
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
