from . import crud, schemas, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


test_engine = create_engine("sqlite:///./test.db")
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

#Create DB Tables
models.Base.metadata.create_all(bind=test_engine)

def test_can_create_project():
    input = {"name": "TestProject"}
    prjCreate: schemas.ProjectCreate = schemas.ProjectCreate(**input)
    db_project = crud.create_project(TestSession(), prjCreate)
    assert db_project is not None
    assert db_project.id > 0
    assert db_project.name == input["name"]
