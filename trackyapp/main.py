from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/projects/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = crud.get_project_by_name(db, project.name)
    if db_project:
        raise HTTPException(status_code=400, detail="Project already registered")
    return crud.create_project(db,project)


@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects


@app.get("/projects/{project_id}", response_model=schemas.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@app.post("/projects/{project_id}/start", response_model=schemas.TrackItem)
def create_trackitem_for_project(project_id: int, item: schemas.TrackItemCreate, db: Session = Depends(get_db)):
    check_item: models.TrackItem = crud.get_active_item_by_project(db,project_id=project_id)
    if check_item:
        raise HTTPException(status_code=404, detail="Item active , stop first")
    return crud.create_project_item(db, item=item, project_id=project_id)


@app.put("/projects/{project_id}/stop", response_model=schemas.TrackItem)
def stop_trackitem_for_project(project_id: int, item: schemas.TrackItemStop, db: Session = Depends(get_db)):
    check_item: models.TrackItem = crud.get_active_item_by_project(db,project_id=project_id)
    if check_item is None:
        raise HTTPException(status_code=404, detail="No active item found")
    if check_item.startTime > item.endTime:
        raise HTTPException(status_code=404, detail="Time is invalid")
    return crud.stop_item(db, item=item, item_id=check_item.id)


@app.get("/items/", response_model=list[schemas.TrackItem])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
